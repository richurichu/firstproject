from io import BytesIO
from os import truncate
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from authenticate.models import Referral
from django.db.models import Q 
from django.db.models.functions import TruncDate
from xhtml2pdf import pisa

from django.template.loader import render_to_string

from .models import ReferralProgram
from store.models import *
from orders.models import *
from cart.models import *
from userprofile.models import *
from django.contrib import messages

# Create your views here.
def admins(request):
    return redirect('admin_dashboard')

def customers(request):
   if request.user.is_superuser:
    if request.GET.get('search') is not None:
            search = request.GET.get('search')
            users = User.objects.filter(username__contains=search)
    else:
            users = User.objects.all()
            context = {
            'users': users
        }
   
    return render(request,'customers.html',context)
   else:
            return render(request,'home.html')
   
def block_user(request,id):
      if request.user.is_superuser:
            
            user = get_object_or_404(User, id=id, is_superuser=False)
            user.is_active = False
            user.save()
            return redirect('customers')
      else:
            return render(request,'home.html')


def unblock_user(request,id):
      if request.user.is_superuser:
            
            user = get_object_or_404(User, id=id, is_superuser=False)
            user.is_active = True
            user.save()
            return redirect('customers')
      else:
            return render(request,'home.html')

def admin_catagory(request):
      if request.user.is_superuser:
             
            cat= Category.objects.order_by('name')
            return render(request,'admin_catagory.html',{'cat':cat})
      else:
            return render(request,'home.html') 
def edit_category(request,id):
      if request.user.is_superuser:
             category=get_object_or_404(Category,id=id)

             if request.method == 'POST':
                   catagory_name = request.POST['name']
                   
                   catagory_discount = int(request.POST['discount'])
                   image = request.FILES.get('image')
                   bannerimage = request.FILES.get('bannerimage')
                   category.discount = catagory_discount
                   if catagory_discount <= 0:
                       messages.error(request, "Discount must be greater than 0.")
                       return render(request, 'category_edit.html', {'category': category})
                   category.name = catagory_name
                   if image:
                     category.image = image
                   if bannerimage:
                     category.bannerimage = bannerimage
                  
                     
                   category.save()
                   
                   return redirect('admin_catagory')
             
             return render(request,'category_edit.html',{'category':category})
      
      else:
            return render(request,'home.html')

def add_category(request):
      if request.user.is_superuser:
           

            if request.method == 'POST':
                  category_name = request.POST['name']
                  
                  category_discount = request.POST['discount']
                  if category_discount <= 0:
                       messages.error(request, "Discount must be greater than 0.")
                       return render(request, 'admin_addcategory.html')
                  image = request.FILES.get('image')
                  bannerimage = request.FILES.get('bannerimage')

                  new_category = Category.objects.create(name=category_name,discount=category_discount,image=image,bannerimage=bannerimage)   
                  new_category.save()
                 

                  return redirect('admin_catagory')
            return render(request,'admin_addcategory.html')
      else:
            return render(request,'home.html')
   


def disable_category(request,id):
      if request.user.is_superuser:

            category = get_object_or_404(Category,id=id)
            category.is_active = False
            category.save()

            return redirect('admin_catagory')
      
      else:
            return render(request,'home.html')
      
def enable_category(request,id):
      if request.user.is_superuser:

            category = get_object_or_404(Category,id=id)
            category.is_active = True
            category.save()

            return redirect('admin_catagory')
      else:
            return render(request,'home.html')
      
def admin_products(request):
      if request.user.is_superuser:

            products = Product.objects.all()
            return render(request,'admin_products.html',{'products':products})
      else:
         return render(request,'home.html')

def admin_varients(request,id):
      if request.user.is_superuser:
      
        product = get_object_or_404(Product,id=id)
        varients= product.productvariant_set.all() 

        context= {
              'product':product,
              'varients': varients
             }
        return render(request,'admin_productvarients.html',context)
      else:
         return render(request,'home.html')
      

def admin_addvarients(request,id):
      if request.user.is_superuser:
            colours= Color.objects.all()
           
            if request.method == 'POST':
               model_name= request.POST['model_name']
               color= request.POST['color']
               store_price= request.POST['store_price']
               sale_price= request.POST['sale_price']
               Discount_price= request.POST['Discount']
               discount_percentage = int(Discount_price)
             
               if discount_percentage < 0:
           
                       messages.error(request, "Discount percentage must be greater than or equal to 0.")
                       return render(request, 'admin_addvariant.html',{'colours':colours})
               
               stock= request.POST['stock']
               product= get_object_or_404(Product,id=id)
               colour, created = Color.objects.get_or_create(color=color)

            # Check if a variant with the same color already exists for the product
               existing_variant = ProductVariant.objects.filter(product=product, color=colour).first()

               if existing_variant:
                 messages.error(request, f"Variant with color '{color}' is already taken , Add another colour.")
                 return render(request, 'admin_addvariant.html', {'colours': colours})
               
               else:

                 new_variant = ProductVariant.objects.create( product= product, model_name= model_name, color= colour,  store_price=store_price,  sale_price =sale_price, discount_percentage = Discount_price, stock=stock)
             


                 variant_images = request.FILES.getlist('images')
                 for img in  variant_images:
                      ProductImage.objects.create( variant=new_variant, image=img)
                   
              
                 return redirect('admin_products')
               

            
            return render(request, 'admin_addvariant.html',{'colours':colours})
      else:
            return render(request,'home.html')
      

def admin_addproduct(request):
      
      if request.user.is_superuser:
            cat= Category.objects.filter(is_active =True)
            
            color= Color.objects.all()
           
            products= Product.objects.all()


            contex ={
                  'cat':cat,
                  'color':color

            }

            if request.method == 'POST':
                  Name = request.POST['name']
                  description = request.POST['shortdescription']
                  created = request.POST['created_at']
                  upadated = request.POST['updated_at']
                  category = request.POST['category']
                  color= request.POST['color']
                  Discount_price= request.POST['discount']
                  discount_percentage = int(Discount_price)
                  
                  if discount_percentage < 0:
           
                       messages.error(request, "Discount percentage must be greater than or equal to 0.")
                       return render(request,'admin_addproduct.html',contex)
                  
                  if Product.objects.filter(name=Name).exists():
                       messages.error(request, "A product with this name already exists.")
                       return render(request,'admin_addproduct.html',contex)

                #   colour, created = Color.objects.get_or_create(color=color)

                #  # Check if a variant with the same color already exists for the product
                #   existing_variant = ProductVariant.objects.filter(product=product, color=colour).first()

                #   if existing_variant:
                #        messages.error(request, f"Variant with color '{color}' is already taken , Add another colour.")
                #        return render(request,'admin_addproduct.html',contex)       


                  cat_id= get_object_or_404(Category, id=category)
                 
                  prod=Product.objects.create(name=Name, shortdescription=description, created_at=created,  updated_at=upadated, category=cat_id )
                  
                 

                  model_name= request.POST['model_name']
                 
                  store_price= request.POST['store_price']
                  sale_price= request.POST['sale_price']
                 
                
                       
                       

                       
                  stock= request.POST['stock']
                  product= get_object_or_404(Product,id=prod.id)

               
                  colour = get_object_or_404(Color,color=color)

                  new_variant = ProductVariant.objects.create( product= product, model_name= model_name, color= colour,  store_price=store_price,  sale_price =sale_price,discount_percentage = Discount_price, stock=stock)
             


                  variant_images = request.FILES.getlist('images')
                  for img in  variant_images:
                      ProductImage.objects.create( variant=new_variant, image=img)
                   
              
                  return redirect('admin_products')
            
            cat= Category.objects.filter(is_active =True)
            
            color= Color.objects.all()

            contex ={
                  'cat':cat,
                  'color':color
            }

            return render(request,'admin_addproduct.html',contex)
      else:
            return render(request,'home.html')
      






def admin_editvarients(request, id):
    if request.user.is_superuser: 
        productt = get_object_or_404(ProductVariant, id=id)
        variants = Product.objects.get(id=productt.product.id) 
        images = ProductImage.objects.filter(variant=productt)
        colors = Color.objects.all()
        exiting_colour= productt.color.color
        
   
        if request.method == 'POST':
           
            color_id = request.POST.get('color')
            colour = get_object_or_404(Color, id=color_id)
           
            if exiting_colour != colour.color:
              

           
              existing_variant = ProductVariant.objects.filter(product=variants, color=colour).first()

              if existing_variant:
                   messages.error(request, f"Variant with color '{colour.color}' is already taken. Please choose another color.")
                   context = {
                    'productt': productt,
                    'variants': variants,
                    'images': images,
                    'color': colors
                  }
                   return render(request, 'admin_editvariant.html', context)

            model_name = request.POST['model_name']
            store_price = request.POST['store_price']
            sale_price = request.POST['sale_price']

          
            discount_percentage = request.POST.get('Discount')
            if discount_percentage == '':
                productt.discount_percentage = None
            else:
                discount_percentage = int(discount_percentage)
                if discount_percentage < 0:
                    messages.error(request, "Discount percentage must be greater than or equal to 0.")
                    context = {
                        'productt': productt,
                        'variants': variants,
                        'images': images,
                        'color': colors
                    }
                    return render(request, 'admin_editvariant.html', context)

                productt.discount_percentage = discount_percentage

            productt.model_name = model_name
            productt.color = colour
            productt.store_price = store_price
            productt.sale_price = sale_price
            productt.stock = request.POST['stock']
            productt.save()

            variant_images = request.FILES.getlist('images')

            if variant_images:
                # Delete existing images and add the new ones
                existing_images = ProductImage.objects.filter(variant=productt)
                existing_images.delete()

                for img in variant_images:
                    ProductImage.objects.create(variant=productt, image=img)

            return redirect('admin_products')

    context = {
        'productt': productt,
        'variants': variants,
        'images': images,
        'color': colors
    }
    return render(request, 'admin_editvariant.html', context)



def admin_disablevarients(request, id):
     if request.user.is_superuser: 
          variant = get_object_or_404(ProductVariant, id=id)
          variant.is_active = False
          variant.save()
          return redirect('admin_products')
     else:
            return render(request,'home.html')
     
def admin_enablevarients(request, id):
     if request.user.is_superuser: 
          variant = get_object_or_404(ProductVariant, id=id)
          variant.is_active = True
          variant.save()
          return redirect('admin_products')

     else:
            return render(request,'home.html')
     

def admin_orders(request):
     if request.user.is_superuser: 
        status = request.GET.get('status')
        if status:
         orders = Order.objects.filter(payment_status=status).order_by('-order_date')
        else:
         orders = Order.objects.all().order_by('-order_date')
     
        
        return render(request ,'admin_order_all.html',{'orders':orders})
          
     else:
            return render(request,'home.html')
              
def order_views(request,order_id):
  if request.user.is_superuser: 
    
    view_order = Order.objects.get(id=order_id)
    order = OrderItem.objects.filter(order=view_order)

    context ={
        'order':order,
        'view_order':view_order,
    }
    return render(request,'admin_order_view.html',context)

  else:
            return render(request,'home.html')
  

def cancel_order(request, order_id):
  if request.user.is_superuser: 
    order = get_object_or_404(Order, id=order_id)

    
        # Update the payment status to 'CANCELLED'
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        
           
            variant = item.product
             
            variant.stock += item.quantity
            

            variant.save()
          

    order.payment_status = 'CANCELLED'
    order.save()

    return redirect('admin_orders')  

  else:
            return render(request,'home.html')
  
def shipped(request, order_id):
    
  if request.user.is_superuser: 
    order = get_object_or_404(Order, id=order_id)

    
        
    
          

    order.payment_status = 'SHIPPED'
    order.save()

    return redirect('admin_orders') 
  else:
            return render(request,'home.html')    

def view_coupon(request):
   if request.user.is_superuser: 
     coupons= Coupon.objects.all()

     return render(request,'admin_view_coupon.html',{'coupons':coupons})   
   else:
            return render(request,'home.html') 
   

def edit_coupon(request, coupon_id):
    
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == 'POST':
        # Update the coupon instance with the form data
         coupon.code = request.POST['code']
         coupon.discount = request.POST['discount']
         coupon.valid_from = request.POST['valid_from']
         coupon.valid_to = request.POST['valid_to']
         coupon.minimum_order_amount = request.POST['minimum_order_amount']
         coupon.is_active = 'is_active' in request.POST
         coupon.single_use_per_user = 'single_use_per_user' in request.POST
         coupon.quantity = request.POST['quantity']

        # Save the updated coupon instance
         coupon.save()

        # Redirect to a success page or show a success message
         return redirect('view_coupon') 
     



    return render(request, 'admin_edit_coupon.html',{'coupon': coupon})
    
def add_coupon(request):
    if request.method == 'POST':
       
        code = request.POST['code']
        discount = request.POST['discount']
        valid_from = request.POST['valid_from']
        valid_to = request.POST['valid_to']
        minimum_order_amount = request.POST['minimum_order_amount']
        is_active = 'is_active' in request.POST
        single_use_per_user = 'single_use_per_user' in request.POST
        quantity = request.POST['quantity']

        # Create a new coupon instance
        new_coupon = Coupon.objects.create(
            code=code,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            minimum_order_amount=minimum_order_amount,
            is_active=is_active,
            single_use_per_user=single_use_per_user,
            quantity=quantity,
        )
       
        new_coupon.save()

       
        return redirect('view_coupon')  

    return render(request, 'add_coupon.html')



def disable_coupon(request, coupon_id):
    if request.user.is_superuser: 

      coupon = get_object_or_404(Coupon, id=coupon_id)
      coupon.is_active = False
      coupon.save()

      return redirect('view_coupon')
    else:
            return render(request,'home.html') 
    

def enable_coupon(request, coupon_id):
   if request.user.is_superuser: 
      coupon = get_object_or_404(Coupon, id=coupon_id)
      coupon.is_active = True
      coupon.save()

      return redirect('view_coupon')
   else:
            return render(request,'home.html') 
   


def order_complete(request, order_id):
   
    order = get_object_or_404(Order, id=order_id)
    referral_program = ReferralProgram.objects.first() 
    referrer_bonus_percentage = referral_program.referrer_bonus_percentage 
    referrer_max_bonus_amount= referral_program.referrer_max_bonus_amount

    referee_bonus_percentage = referral_program.referee_bonus_percentage
    referee_max_bonus_amount = referral_program.referee_max_bonus_amount
    bonus_amount_1 = 0
    bonus_amount_2 = 0

    user = order.user
   
    total = Decimal(order.total_price) 
   
    

    
    has_completed_order = Order.objects.filter(user=user, payment_status='COMPLETED').exists()

    if not has_completed_order:
        buyer_wallet = Wallet.objects.get(user=user)

        try:
            referral = Referral.objects.get(user=user)

           
            referral_wallet = Wallet.objects.get(user=referral.referred_by)
            bonus_amount_1 = total * (referrer_bonus_percentage / 100)
            if bonus_amount_1 < referrer_max_bonus_amount:
              referral_wallet.balance += bonus_amount_1  
            else:
              referral_wallet.balance += referrer_max_bonus_amount 
              
            referral_wallet.save()

            bonus_amount_2 = total * (referee_bonus_percentage / 100)
            if bonus_amount_2 < referee_max_bonus_amount:
              buyer_wallet.balance += bonus_amount_2  
            else:
              buyer_wallet.balance += referee_max_bonus_amount  
        
            buyer_wallet.save()


        except Referral.DoesNotExist:
             messages.warning(request, "Referral does not exist for this user.")
            

       
        
        order.payment_status = 'COMPLETED'
        order.save()
   
    return redirect('admin_orders') 



def edit_referral_program(request):
  if request.user.is_superuser: 
    referral_program = ReferralProgram.objects.first()  

    if request.method == 'POST':
       
        description = request.POST.get('description')
        referrer_bonus_percentage = request.POST.get('referrer_bonus_percentage')
        referrer_max_bonus_amount = request.POST.get('referrer_max_bonus_amount')
        referee_bonus_percentage = request.POST.get('referee_bonus_percentage')
        referee_max_bonus_amount = request.POST.get('referee_max_bonus_amount')

       
        referral_program.description = description
        referral_program.referrer_bonus_percentage = referrer_bonus_percentage
        referral_program.referrer_max_bonus_amount = referrer_max_bonus_amount
        referral_program.referee_bonus_percentage = referee_bonus_percentage
        referral_program.referee_max_bonus_amount = referee_max_bonus_amount

        
        referral_program.save()

        return redirect('admin_view_referral') 

    return render(request, 'admin_refer_edit.html', {'referral_program': referral_program})
  else:
            return render(request,'home.html')  



def admin_view_referral(request):
    referral_program = ReferralProgram.objects.first()  # Assuming you have only one ReferralProgram instance
    return render(request, 'admin_referal_view.html', {'referral_program': referral_program})    



# def add_new_referral_offer(request):
#     if request.method == 'POST':
#         description = request.POST.get('description')
#         referrer_bonus_percentage = request.POST.get('referrer_bonus_percentage')
#         referrer_max_bonus_amount = request.POST.get('referrer_max_bonus_amount')
#         referee_bonus_percentage = request.POST.get('referee_bonus_percentage')
#         referee_max_bonus_amount = request.POST.get('referee_max_bonus_amount')

#         # Create a new ReferralProgram instance with the submitted data
#         ReferralProgram.objects.create(
#             description=description,
#             referrer_bonus_percentage=referrer_bonus_percentage,
#             referrer_max_bonus_amount=referrer_max_bonus_amount,
#             referee_bonus_percentage=referee_bonus_percentage,
#             referee_max_bonus_amount=referee_max_bonus_amount
#         )

#         return redirect('admin_view_referral')

#     return render(request, 'add_new_referral_offer.html')


def add_colour(request):
    if request.method == 'POST':
           color= request.POST.get('colour')
           new_colour= Color(color=color)
           new_colour.save()
           return redirect('admin_products') 
    return render(request, 'admin_add_colour.html')

     
     
def add_banner(request):
     if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        banner = Banner(name=name, image=image)
        banner.save()
        return redirect('list_banners')  # Replace 'list_banners' with the URL name for listing all banners
     return render(request, 'admin_banner_add.html')

def list_banners(request):
     banner= Banner.objects.all()
     return render(request,'list_banner.html',{'banner':banner})

def delete_banner(request,banner_id):
     banner = get_object_or_404(Banner,id=banner_id)
     banner.delete()
     return redirect('list_banners')

def edit_banner(request,banner_id):
     try:
        banner = Banner.objects.get(id=banner_id)
     except Banner.DoesNotExist:
        return HttpResponse("Banner not found.", status=404)

     if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        banner.name = name
        if image:
            banner.image = image
        banner.save()
        return redirect('list_banners') 

     return render(request, 'edit_banner.html', {'b': banner})


def admin_dashboard(request):
     
      if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date and not end_date:
            # Calculate the current date
            current_date = timezone.now().date()

            # Calculate the date 30 days back from the current date
            default_start_date = current_date - timedelta(days=30)
            default_end_date = current_date

            # Convert to string format (YYYY-MM-DD)
            start_date = default_start_date.strftime('%Y-%m-%d')
            end_date = default_end_date.strftime('%Y-%m-%d')

        if start_date and end_date:
            # Corrected query filter for start_date and end_date using 'date' lookup
            order_count_date = Order.objects.filter(
                Q(order_date__date__gte=start_date, order_date__date__lte=end_date) |
                Q(order_date__date=end_date,  order_date__isnull=True)
            ).exclude(payment_status='CANCELLED').count()

            total_price_date = Order.objects.filter(
                Q(order_date__date__gte=start_date, order_date__date__lte=end_date) |
                Q(order_date__date=end_date,  order_date__isnull=True)
            ).exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']

            daily_totals = Order.objects.filter(
                Q(order_date__date__gte=start_date, order_date__date__lte=end_date) |
                Q(order_date__date=end_date, order_date__isnull=True)
            ).exclude(payment_status='CANCELLED').annotate(date=TruncDate('order_date')).values('date').annotate(
                total=Sum('total_price')).order_by('date')

            order_count = Order.objects.exclude(payment_status='CANCELLED').count()
            total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']
            today = timezone.now().date()
            today_orders = Order.objects.filter(order_date__date=today)
            order_count_today = today_orders.count()
            total_price_today = sum(order.total_price for order in today_orders)
            recent_orders = Order.objects.order_by('-order_date')[:3]

            # Corrected query for top_selling_products using 'product_id' and 'product__name'
            top_selling_products = OrderItem.objects.values('product__product__name').annotate(
                total_quantity=Sum('quantity')
            ).order_by('-total_quantity')[:5]

            categories = Category.objects.all()
            data = []

            for category in categories:
                product_count = Product.objects.filter(category=category).count()
                data.append(product_count)

            context = {
                'order_count_date': order_count_date,
                'total_price_date': total_price_date,
                'start_date': start_date,
                'end_date': end_date,
                'daily_totals': daily_totals,
                'order_count': order_count,
                'total_price': total_price,
                'categories': categories,
                'data': data,
                'order_count_today': order_count_today,
                'total_price_today': total_price_today,
                'recent_orders': recent_orders,
                'top_selling_products': top_selling_products,
            }

            return render(request, 'admin_dashboard.html', context)

        else:
            order_count = Order.objects.exclude(payment_status='CANCELLED').count()
            total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']

            today = timezone.now().date()
            today_orders = Order.objects.filter(order_date__date=today)
            order_count_today = today_orders.count()
            total_price_today = sum(order.total_price for order in today_orders)

            categories = Category.objects.all()
            data = []

            for category in categories:
                product_count = Product.objects.filter(category=category).count()
                data.append(product_count)

            recent_orders = Order.objects.order_by('-order_date')[:3]

            # Corrected query for top_selling_products using 'product_id' and 'product__name'
            top_selling_products = OrderItem.objects.values('product_product_name').annotate(
                total_quantity=Sum('quantity')
            ).order_by('-total_quantity')[:5]

            context = {
                'order_count': order_count,
                'total_price': total_price,
                'start_date': start_date,
                'end_date': end_date,
                'order_count_today': order_count_today,
                'total_price_today': total_price_today,
                'categories': categories,
                'data': data,
                'recent_orders': recent_orders,
                'top_selling_products': top_selling_products,
            }

            return render(request, admin_dashboard.html,context)

      return HttpResponseBadRequest("Invalid request method.")

def pdf_view(request):

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Today's totals
    today_orders = Order.objects.filter(order_date__date=today)
    order_count_today = today_orders.count()
    total_price_today = today_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Weekly totals
    week_orders = Order.objects.filter(order_date__date__range=[week_ago, today])
    order_count_week = week_orders.count()
    total_price_week = week_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Monthly totals
    month_orders = Order.objects.filter(order_date__date__range=[month_ago, today])
    order_count_month = month_orders.count()
    total_price_month = month_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Top selling products
    top_selling_products_today = OrderItem.objects.values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_week = OrderItem.objects.filter(order_id__order_date__date__range=[week_ago, today]).values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_month = OrderItem.objects.filter(order_id__order_date__date__range=[month_ago, today]).values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    context = {
        'order_count_today': order_count_today,
        'total_price_today': total_price_today,
        'order_count_week': order_count_week,
        'total_price_week': total_price_week,
        'order_count_month': order_count_month,
        'total_price_month': total_price_month,
        'top_selling_products_today': top_selling_products_today,
        'top_selling_products_week': top_selling_products_week,
        'top_selling_products_month': top_selling_products_month,
    }

    return render(request, 'pdf_view.html',context)
     

def download_order_pdf_sales(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Today's totals
    today_orders = Order.objects.filter(order_date__date=today)
    order_count_today = today_orders.count()
    total_price_today = today_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Weekly totals
    week_orders = Order.objects.filter(order_date__date__range=[week_ago, today])
    order_count_week = week_orders.count()
    total_price_week = week_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Monthly totals
    month_orders = Order.objects.filter(order_date__date__range=[month_ago, today])
    order_count_month = month_orders.count()
    total_price_month = month_orders.aggregate(Sum('total_price'))['total_price__sum']

    # Top selling products
    top_selling_products_today = OrderItem.objects.values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_week = OrderItem.objects.filter(order_id__order_date__date__range=[week_ago, today]).values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_selling_products_month = OrderItem.objects.filter(order_id__order_date__date__range=[month_ago, today]).values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    context = {
        'order_count_today': order_count_today,
        'total_price_today': total_price_today,
        'order_count_week': order_count_week,
        'total_price_week': total_price_week,
        'order_count_month': order_count_month,
        'total_price_month': total_price_month,
        'top_selling_products_today': top_selling_products_today,
        'top_selling_products_week': top_selling_products_week,
        'top_selling_products_month': top_selling_products_month,
    }

    
    html_content = render_to_string('pdf_download.html', context)

    # Set the response content type as 'application/pdf' to indicate that it's a PDF file
    response = HttpResponse(content_type='application/pdf')

    # Set the filename for the downloaded file
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    # Generate the PDF content from the HTML using xhtml2pdf
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), response)
    
    if pdf.err:
        return HttpResponse('Error generating PDF', status=500)

    return response