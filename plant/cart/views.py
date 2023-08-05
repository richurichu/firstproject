from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from store.models import *
from userprofile.models import *
from django.views.decorators.cache import never_cache



def create_or_get_cart(request):
   
    if request.user.is_authenticated:
    # if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
       
        if  session_key is None:
            request.session.save()
            session_key = request.session.session_key
           
        cart, _ = Cart.objects.get_or_create(user=None, session_key= session_key)

       
    return cart     


def add_to_cart(request, variant_id):
   
    variant = ProductVariant.objects.get(id=variant_id)
    discounted_price, _ = variant.get_discounted_price()

    cart  = create_or_get_cart(request)

    item, created = cart.cartitems_set.get_or_create(
        product=variant,
        defaults={'price': discounted_price, 'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.price = discounted_price * item.quantity
        item.save()

    return redirect('view_cart')

@never_cache
def view_cart(request):
   
   
    final_price=0
    cart= create_or_get_cart(request)
    total_price = cart.get_total_price()  # Calculate the new total price
    if total_price is None:
      total_price = Decimal(0)
      
    request.session['total'] = str(total_price)
    coupon = Decimal(request.session.get('coupon', '0'))
    if coupon>0:
        final_price=total_price-coupon
    else:
        final_price=total_price
    request.session['final'] = str(final_price)

   
    
   
    cart_items = cart.cartitems_set.all()
   
     
    discounted_price = 0  
    
   

    if cart_items:
   
     coupons = Coupon.objects.filter(is_active=True, minimum_order_amount__lte=total_price)
        

     context = {
            'cart': cart,
            'total_price': total_price,
            'discounted_price': discounted_price,
            
            'coupons': coupons,
            
     }

     return render(request, 'cart_view.html', context)
    else:
        return render(request, 'empty_cart.html')





          



def apply_coupon(request):
    
    cart = create_or_get_cart(request)

    cart_items = cart.cartitems_set.all()
   
    coupon_applied_total=0
    total_price = Decimal(request.session['total'])
    

    coupons = Coupon.objects.filter(is_active= True)    
    

    if request.method == 'POST':
       
        selected_coupon_code = request.POST.get('coupon_code')
        if not selected_coupon_code:
         return JsonResponse({
            'success': False,
            'message': 'No coupon selected.',
         })
       
        
        
        selected_coupon = Coupon.objects.get(code=selected_coupon_code)
        


        if selected_coupon_code:
           
            selected_coupon = get_object_or_404(Coupon, code=selected_coupon_code)
            if selected_coupon.minimum_order_amount <= total_price  :
               
               coupon_applied_total = total_price - selected_coupon.discount
               coupon_discount=total_price-coupon_applied_total
               request.session['coupon'] = str(coupon_discount)
               request.session['final'] = str(coupon_applied_total)
              
               return JsonResponse({
                    'success': True,
                    'coupon_code': selected_coupon_code,
                    'final_price': float(coupon_applied_total),
                    'coupon_discount': float(coupon_discount)

                })
            
            else:
              selected_coupon.discount=0
              selected_coupon_code= None
              return JsonResponse({
                    'success': False,
                    'message': 'Failed to apply coupon'
              })
    

    else:
    # If not a POST request, return available coupons
      coupons = Coupon.objects.filter(is_active=True, minimum_order_amount__lte=total_price)
      coupons_list = list(coupons.values())  # Convert QuerySet to list of dictionaries
      return JsonResponse(coupons_list, safe=False)        
    # return render(request, 'cart_view.html', context)

    
   


    
def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
       
        cart_item = CartItems.objects.get(id=item_id)
        cart_item.delete()

        return redirect('view_cart')

    # return render(request, 'cart_view.html')
    return redirect('view_cart')


    

def update_quantity(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        
        product = CartItems.objects.get(id=product_id)
        product.quantity = quantity
        product.price = product.discounted_item_price 
       

        product.save()

        cart = product.cart  # Retrieve the cart object
        total_price = cart.get_total_price()  # Calculate the new total price
        request.session['total'] = str(total_price)
        
        final_price=total_price
        request.session['final'] = str(final_price)
        coupon=0
        request.session['coupon'] = str(coupon)
        
        

        response_data = {
            'success': True,
            'message': 'Quantity updated successfully!',
            'price': str(product.price),
            'quantity': str(product.quantity),
            'total_price': str(total_price),
            'coupon': str(coupon),
        }

        return JsonResponse(response_data)
    
    response_data = {
        'success': False,
        'message': 'Invalid request',
    }
    
    return JsonResponse(response_data, status=400)



def add_to_whishlist(request, variant_id):
      
      if not request.user.is_authenticated:
          
          return redirect('signin')
      variant = ProductVariant.objects.get(id=variant_id)

      wishlist, created = Wishlist.objects.get_or_create(user=request.user)
      item = wishlist.wishlistitem_set.filter(product=variant)

      if item.exists():
    
          return redirect('view_wishlist')
      else:
           WishlistItem.objects.create(wishlist = wishlist, product=variant)
           return redirect('view_wishlist')

def remove_wish(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    wishlist = get_object_or_404(Wishlist,user=request.user)
    item = wishlist.wishlistitem_set.filter(product=variant)

    if item.exists():
      item.delete()

    return redirect('view_wishlist')


    

def view_wishlist(request):
    wishlist= get_object_or_404(Wishlist, user=request.user)
    user_products = CartItems.objects.filter(cart__user= request.user).values_list('product__id' , flat=True)
    items= WishlistItem.objects.filter( wishlist= wishlist)
   
    return render(request, 'view_wishlist.html', {'wishlist': wishlist, 'items': items, 'user_products':user_products})



   

