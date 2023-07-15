from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from store.models import *
from orders.models import *
from cart.models import *

# Create your views here.
def admins(request):
    return render(request,'admin_base.html')

def customers(request):
    if request.GET.get('search') is not None:
            search = request.GET.get('search')
            users = User.objects.filter(username__contains=search)
    else:
            users = User.objects.all()
            context = {
            'users': users
        }
   
    return render(request,'customers.html',context)
def block_user(request,id):
      if request.user.is_superuser:
            
            user = get_object_or_404(User, id=id, is_superuser=False)
            user.is_active = False
            user.save()
            return redirect('customers')
      else:
            return redirect('customers')


def unblock_user(request,id):
      if request.user.is_superuser:
            
            user = get_object_or_404(User, id=id, is_superuser=False)
            user.is_active = True
            user.save()
            return redirect('customers')
      else:
            return redirect('customers')

def admin_catagory(request):
      if request.user.is_superuser:
             
            cat= Category.objects.order_by('name')
            return render(request,'admin_catagory.html',{'cat':cat})
       
def edit_category(request,id):
      if request.user.is_superuser:
             category=get_object_or_404(Category,id=id)

             if request.method == 'POST':
                   catagory_name = request.POST['name']
                   image = request.FILES.get('image')
                   bannerimage = request.FILES.get('bannerimage')
                   
                   category.name = catagory_name
                   if image:
                     category.image = image
                   if bannerimage:
                     category.bannerimage = bannerimage
                   
                   category.save()
                   
                   return redirect('admin_catagory')
             
             return render(request,'category_edit.html',{'category':category})
      
      else: return redirect('admin_catagory')

def add_category(request):
      if request.user.is_superuser:
           

            if request.method == 'POST':
                  category_name = request.POST['name']
                  image = request.FILES.get('image')
                  bannerimage = request.FILES.get('bannerimage')

                  new_category = Category.objects.create(name=category_name,image=image,bannerimage=bannerimage)   
                  new_category.save()
                 

                  return redirect('admin_catagory')
            return render(request,'admin_addcategory.html')
      return render('admin_catagory')
   


def disable_category(request,id):
      if request.user.is_superuser:

            category = get_object_or_404(Category,id=id)
            category.is_active = False
            category.save()

            return redirect('admin_catagory')
      
def enable_category(request,id):
      if request.user.is_superuser:

            category = get_object_or_404(Category,id=id)
            category.is_active = True
            category.save()

            return redirect('admin_catagory')
      
def admin_products(request):
      if request.user.is_superuser:

            products = Product.objects.all()
            return render(request,'admin_products.html',{'products':products})


def admin_varients(request,id):
      if request.user.is_superuser:
      
        product = get_object_or_404(Product,id=id)
        varients= product.productvariant_set.all() 

        context= {
              'product':product,
              'varients': varients
             }
        return render(request,'admin_productvarients.html',context)
      
def admin_addvarients(request,id):
      if request.user.is_superuser:
           
            if request.method == 'POST':
               model_name= request.POST['model_name']
               color= request.POST['color']
               store_price= request.POST['store_price']
               sale_price= request.POST['sale_price']
               stock= request.POST['stock']
               product= get_object_or_404(Product,id=id)

               
               colour = get_object_or_404(Color,color=color)

               new_variant = ProductVariant.objects.create( product= product, model_name= model_name, color= colour,  store_price=store_price,  sale_price =sale_price, stock=stock)
             


               variant_images = request.FILES.getlist('images')
               for img in  variant_images:
                    ProductImage.objects.create( variant=new_variant, image=img)
                   
              
               return redirect('admin_products')
               

            colours= Color.objects.all()
            return render(request, 'admin_addvariant.html',{'colours':colours})

def admin_addproduct(request):
      if request.user.is_superuser:
            if request.method == 'POST':
                  Name = request.POST['name']
                  description = request.POST['shortdescription']
                  created = request.POST['created_at']
                  upadated = request.POST['updated_at']
                  category = request.POST['category']
                  cat_id= get_object_or_404(Category, name=category)
                  prod=Product.objects.create(name=Name, shortdescription=description, created_at=created,  updated_at=upadated, category=cat_id )
                  
                 

                  model_name= request.POST['model_name']
                  color= request.POST['color']
                  store_price= request.POST['store_price']
                  sale_price= request.POST['sale_price']
                  stock= request.POST['stock']
                  product= get_object_or_404(Product,id=prod.id)

               
                  colour = get_object_or_404(Color,color=color)

                  new_variant = ProductVariant.objects.create( product= product, model_name= model_name, color= colour,  store_price=store_price,  sale_price =sale_price, stock=stock)
             


                  variant_images = request.FILES.getlist('images')
                  for img in  variant_images:
                      ProductImage.objects.create( variant=new_variant, image=img)
                   
              
                  return redirect('admin_products')
            
            cat= Category.objects.all()
            color= Color.objects.all()

            contex ={
                  'cat':cat,
                  'color':color
            }

            return render(request,'admin_addproduct.html',contex)

def admin_editvarients(request, id):
      if request.user.is_superuser: 

            if request.method == 'POST':
               print('======')
               model_name= request.POST['model_name']
               color= request.POST['color']
               store_price= request.POST['store_price']
               sale_price= request.POST['sale_price']
               stock= request.POST['stock']
               productt = get_object_or_404(ProductVariant, id=id)
               variants = Product.objects.get(id=productt.product.id) 
               product= get_object_or_404(Product,id=variants.id)
               
               


               
               colour = Color.objects.get(id=color)
              

               new_variant = ProductVariant.objects.create( product= product, model_name= model_name, color= colour,  store_price=store_price,  sale_price =sale_price, stock=stock)
             


               variant_images = request.FILES.getlist('images')
               for img in  variant_images:
                    ProductImage.objects.create( variant=new_variant, image=img)
                   
              
               return redirect('admin_products')
            
      productt = get_object_or_404(ProductVariant, id=id)
      variants = Product.objects.get(id=productt.product.id) 
      images= ProductImage.objects.filter(variant=productt)
      color= Color.objects.all()
   
      context = {
        'productt': productt,
        'variants': variants,
        'images':images,
        'color':color
    }
      return render(request, 'admin_editvariant.html', context)

def admin_disablevarients(request, id):
     if request.user.is_superuser: 
          variant = get_object_or_404(ProductVariant, id=id)
          variant.is_active = False
          variant.save()
          return redirect('admin_products')

def admin_enablevarients(request, id):
     if request.user.is_superuser: 
          variant = get_object_or_404(ProductVariant, id=id)
          variant.is_active = True
          variant.save()
          return redirect('admin_products')


def admin_orders(request):
     if request.user.is_superuser: 
     
          orders = Order.objects.all()
          return render(request ,'admin_order_all.html',{'orders':orders})
          
     
              
def order_views(request,order_id):
    view_order = Order.objects.get(id=order_id)
    order = OrderItem.objects.filter(order=view_order)

    context ={
        'order':order
    }
    return render(request,'admin_order_view.html',context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.payment_status != 'PAID' and order.payment_status != 'CANCELLED':
        # Update the payment status to 'CANCELLED'
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
        
            print(item.quantity)
            variant = item.product  
            variant.stock += item.quantity
            variant.save()
          

        order.payment_status = 'CANCELLED'
        order.save()

    return redirect('admin_orders')        
      
     