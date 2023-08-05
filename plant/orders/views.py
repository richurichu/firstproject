from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from cart.models import *
from userprofile.models import*
from django.template.loader import render_to_string
from io import BytesIO
import razorpay
from xhtml2pdf import pisa
from .models import*
from django.shortcuts import get_object_or_404
from decimal import Decimal 

# Create your views here.

def checkout(request,add_id):
    user_address= get_object_or_404(User_address, id= add_id, user= request.user)
    carts = get_object_or_404(Cart,user=request.user)
    # item =  CartItems.objects.filter(cart=carts)
    # original=0
    # for  single in item:
    #   original = original + single.item_price
      
    
    # total_price = carts.get_total_price()
    
    # total_price= request.session.get('coupon_applied_total',0)
    # discount= request.session.get('discount',0)
    # coupon= request.session.get('selected_coupon',0)
    # total= request.session.get('total',0)
    total_price = Decimal(request.session.get('total', '0'))  
    
   
    final_price = Decimal(request.session.get('final', '0'))
    coupon = Decimal(request.session.get('coupon', '0'))

    if total_price>500:
        total_price_delivery=final_price
    else:
        total_price_delivery=final_price + 40
    
    request.session['final_price'] = str(total_price_delivery)
   
    
    return render(request,'final_checkout.html',{'user_address': user_address, 'carts':carts, 'total_price_delivery':total_price_delivery,'total_price':total_price,  'coupon':coupon , 'final':final_price })

def placeorder(request, add_id):
   
    user_address= get_object_or_404(User_address, id= add_id, user= request.user)
    carts = get_object_or_404(Cart,user=request.user)
    item =  CartItems.objects.filter(cart=carts)
    if item.exists():

            original=0
            for  single in item:
              original = original + single.item_price
            # total_price = sum(item.price * item.quantity for item in item)
            request.session['original'] = str(original)
            coupon = Decimal(request.session.get('coupon', '0'))
            total_price=  Decimal(request.session.get('final_price', '0'))
            final_price = Decimal(request.session.get('final', '0'))
            
            order = Order.objects.create(
                user=request.user,
                address=user_address,
                total_price=final_price,
                original_price= original,
                coupon=coupon,
                payment_status='ORDERED',
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
    else:
        return render(request,'orderplaced.html')


def orders(request):
    orders= Order.objects.filter(user= request.user).order_by('-id')

    return render(request,'ordertable.html',{'orders':orders})


def order_view(request,order_id):
    orderr= Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=orderr)
   
    discount= orderr.original_price-(orderr.total_price+orderr.coupon)
    if orderr.total_price <=500:
      actuall_total=orderr.total_price +40
      shipping=40
    else:
      actuall_total=orderr.total_price
      shipping = 0
    


    return render(request,'orderview.html',{'order_item':order_item ,'orderr':orderr,'discount':discount,'actuall_total':actuall_total,'shipping':shipping})


def cancel_orderss(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.payment_status != 'CANCELLED':
          if order.payment_method=='RAZORPAY':
            user = order.user
            refund= Decimal(order.total_price)
            user_wallet = get_object_or_404(Wallet,user= user)
            user_wallet.balance += refund 
            user_wallet.save()

          order_items = OrderItem.objects.filter(order=order)

          for item in order_items:
              variant= item.product
              variant.stock = variant.stock + item.quantity
              variant.save()
   
            
          order.payment_status = 'CANCELLED'
          order.save()
       

    return redirect('orders')

def Return_orderss(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    user = order.user
    refund= Decimal(order.total_price)
    user_wallet = get_object_or_404(Wallet,user= user)
    user_wallet.balance += refund 
    user_wallet.save()

    if order.payment_status != 'CANCELLED':
          order_items = OrderItem.objects.filter(order=order)

          for item in order_items:
              variant= item.product
              variant.stock = variant.stock + item.quantity
              variant.save()
   
            
          order.payment_status = 'RETURNED'
          order.save()
       

    return redirect('orders')
    

def initiate_payment(request):
    
    if request.method == 'POST':
        # Retrieve the total price and other details from the backend
        # cart = Cart.objects.get(user_id=request.user)
        # cart_items = cart.cartitems_set.all()

       
        total_price_str = request.session.get('final_price', '0.00')
        total_price = Decimal(total_price_str)

        total_amount_in_cents = int(total_price*100)
        

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({

            'amount': total_amount_in_cents,
            'currency': 'INR',
            'payment_capture': 1

        })

        response_data = {
            'order_id': payment['id'],
            'amount': payment['amount'],
            'currency': payment['currency'],
            'key': settings.RAZOR_KEY_ID,

        }
        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})


def online_payment_order(request, add_id):
    if request.method == 'POST':
        
        payment_id = request.POST.getlist('payment_id')[0]
        orderId = request.POST.getlist('orderId')[0]
        signature = request.POST.getlist('signature')[0]
        user_address = get_object_or_404(User_address, id=add_id, user=request.user)
        cart = Cart.objects.get(user_id=request.user)
        cart_items = cart.cartitems_set.all()

        final_price = Decimal(request.session.get('final', '0'))
        coupon = Decimal(request.session.get('coupon', '0'))
        # total_price_str = request.session.get('final_price', '0.00')
        total_price = Decimal(final_price)
        original_price=  Decimal(request.session.get('final_price', '0'))
        order = Order.objects.create(
            user=request.user,
            address=user_address,
            total_price=total_price,
            original_price= original_price,
            payment_status='ORDERED',
            payment_method='RAZORPAY',
            coupon=coupon,
            razor_pay_payment_id=payment_id,
            razor_pay_payment_signature=signature,
            razor_pay_order_id=orderId,
            
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity
            )
            variant = cart_item.product
            variant.stock -= cart_item.quantity
            variant.save()

        cart_items.delete()
        orderId = order.id


        return JsonResponse({'message': 'Order placed successfully', 'orderId': orderId})
    else:
        # Handle invalid request method (GET, etc.)
        return JsonResponse({'error': 'Invalid request method'})
    
# def invoice_download(request,order_id):
#     orderr= Order.objects.get(id=order_id)
#     order_item = OrderItem.objects.filter(order=orderr)
#     discount= orderr.original_price-orderr.total_price
#     actuall_total=orderr.total_price-orderr.coupon


#     return render(request,'show_invoice.html',{'order_item':order_item ,'orderr':orderr,'discount':discount,'actuall_total':actuall_total})
def invoice_download_start(request,order_id):
    orderr= Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=orderr)
    discount= orderr.original_price-orderr.total_price
    actuall_total=orderr.total_price-orderr.coupon

    html_content = render_to_string('invoice_download.html', {'order_item':order_item ,'orderr':orderr,'discount':discount,'actuall_total':actuall_total})

    # Set the response content type as 'application/pdf' to indicate that it's a PDF file
    response = HttpResponse(content_type='application/pdf')

    # Set the filename for the downloaded file
    response['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'

    # Generate the PDF content from the HTML using xhtml2pdf
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), response)
    
    if pdf.err:
        return HttpResponse('Error generating PDF', status=500)

    return response


   