from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import CartItems
from cart.models import WishlistItem

from  .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Min, Max





# Create your views here.
def home(request):
    cat=Category.objects.filter( is_active = True)
    bannner = Banner.objects.all()
    hot_deals_varients=ProductVariant.objects.filter(is_active=True).exclude(discount_percentage__isnull=True).order_by('-discount_percentage')[:4]
    new_arrival_varients = ProductVariant.objects.filter(product__category__name__icontains ='in').distinct('product')[:4]
   
   


    return render(request,'home.html',{'cat': cat ,'banner':bannner ,'hot_deals_varients':hot_deals_varients,'new_arrival_varients':new_arrival_varients})

def cat(request, slug):
    if slug == 'all':
        
        products = Product.objects.all() 
        cat = None
    else:
        cat = get_object_or_404(Category, slug=slug)
        products = cat.product_set.all() 

    price_range = request.GET.get('price_range')
    if price_range:
        min_price, max_price = price_range.split('-')
        products = products.filter(productvariant__sale_price__gte=min_price, productvariant__sale_price__lte=max_price)


    sort_by = request.GET.get('sort')
    if sort_by == 'az':
        products = products.order_by('name')  
    elif sort_by == 'za':
        products = products.order_by('-name') 
   
    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'catagory.html', {'products': products , 'cat':cat})


def product_detail(request, slug):
    productt = get_object_or_404(ProductVariant, slug=slug)
    
    if request.user.is_authenticated:
       user_products = CartItems.objects.filter(cart__user= request.user).values_list('product__id' , flat=True)
       user_wish_products = WishlistItem.objects.filter(wishlist__user= request.user).values_list('product__id' , flat=True)
    else:
        user_products = []
        user_wish_products = []

    variants = Product.objects.get(slug=productt.product.slug) 
    images=    ProductImage.objects.filter(variant=productt)
   
    context = {
        'productt': productt,
        'variants': variants,
        'images':images,
        'user_products':user_products,
        'user_wish_products':user_wish_products,
    }
    return render(request, 'product_details.html', context)

def search(request):
    if request.method == "GET":
        query= request.GET.get('query')

        if query :
            products = Product.objects.filter(name__icontains=query)
            if products:
             return render(request,'catagory.html', {'products': products})
            else:
             messages.info(request, 'No results found.')
    
        
            return redirect('cat','all')
        else:
             messages.info(request, 'Please enter a search query.')
        return redirect('cat','all')
    return render(request, 'catagory.html' )

def autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return render(request, 'catagory.html')

