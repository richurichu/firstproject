from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from store.models import *

# Create your views here.
def add_to_cart(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item = cart.cartitems_set.filter(product=variant).first()

    if item:
        item.quantity += 1
        item.save()

    else:
        CartItems.objects.create(cart=cart, product=variant, quantity=1, price=variant.sale_price)

    return redirect('view_cart') 




def view_cart(request):
    cart = Cart.objects.get(user=request.user)

    # Calculate the total price
    total_price = 0
    cart_items = cart.cartitems_set.all()
    for item in cart_items:
        # Update the price of each item based on the quantity
        item.price = item.product.sale_price * item.quantity
        item.save()

        # Add the item price to the total price
        total_price += item.price

    context = {
        'cart': cart,
        'total_price': total_price
    }

    return render(request, 'cart_view.html', context)

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
       
        cart_item = CartItems.objects.get(id=item_id)
        cart_item.delete()

        return redirect('view_cart')

    return render(request, 'cart_view.html')

def update_quantity(request):
    print(request.method)
    print("header",request.headers.get('HTTP_X_REQUESTED_WITH'))
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        print(quantity)
        
        product = CartItems.objects.get(id=product_id)
        product.quantity = quantity
        product.price = product.product.sale_price * Decimal(product.quantity)
        product.save()
        
        # Prepare the response data
        response_data = {
            'success': True,
            'message': 'Quantity updated successfully!',
            'price': str(product.price),
            'quantity': str(product.quantity),
        }

        return JsonResponse(response_data)
    
    response_data = {
        'success': False,
        'message': 'Invalid request',
    }
    
    return JsonResponse(response_data, status=400)

