from django.shortcuts import redirect, render
from cart.models import *
from userprofile.models import*
from .models import*
from django.shortcuts import get_object_or_404

# Create your views here.

def checkout(request,add_id):
    user_address= get_object_or_404(User_address, id= add_id, user= request.user)
    carts = get_object_or_404(Cart,user=request.user)
    
    return render(request,'checkout.html',{'user_address': user_address, 'carts':carts})

def placeorder(request, add_id):
    user_address= get_object_or_404(User_address, id= add_id, user= request.user)
    carts = get_object_or_404(Cart,user=request.user)
    item =  CartItems.objects.filter(cart=carts)
    total_price = sum(item.price * item.quantity for item in item)

    order = Order.objects.create(
        user=request.user,
        address=user_address,
        total_price=total_price,
        payment_status='PENDING',
        payment_method='CASH_ON_DELIVERY',
    )
    
    for cart_item in item:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            price=cart_item.price,
            quantity=cart_item.quantity
        )
        variant = cart_item.product
        variant.stock -= cart_item.quantity
        variant.save()
    item.delete()

    return render(request,'orderplaced.html')

def orders(request):
    orders= Order.objects.filter(user= request.user)

    return render(request,'ordertable.html',{'orders':orders})


def order_view(request,order_id):
    orderr= Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=orderr)


    return render(request,'orderview.html',{'order_item':order_item})


def cancel_orderss(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.payment_status != 'PAID' and order.payment_status != 'CANCELLED':
          order_items = OrderItem.objects.filter(order=order)

          for item in order_items:
              variant= item.product
              variant.stock = variant.stock + item.quantity
              variant.save()
   
            
          order.payment_status = 'CANCELLED'
          order.save()
       

    return redirect('orders')
    