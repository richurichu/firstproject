from django.shortcuts import get_object_or_404, redirect, render
from  .models import *
from django.contrib import messages
from django.core.paginator import Paginator




# Create your views here.
def home(request):
    cat=Category.objects.filter( is_active = True)
    bannner = Banner.objects.all()
    return render(request,'home.html',{'cat': cat ,'banner':bannner})

def cat(request, slug):
    if slug == 'all':
        
        products = Product.objects.all()  # Retrieve all products
        cat = None
    else:
        cat = get_object_or_404(Category, slug=slug)
        products = cat.product_set.all()  # Retrieve products based on the category

    price_range = request.GET.get('price_range')
    if price_range:
        min_price, max_price = price_range.split('-')
        products = products.filter(productvariant__sale_price__gte=min_price, productvariant__sale_price__lte=max_price)



    paginator = Paginator(products, 8) 

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'catagory.html', {'products': products , 'cat':cat})


def product_detail(request, slug):
    productt = get_object_or_404(ProductVariant, slug=slug)
    variants = Product.objects.get(slug=productt.product.slug) 
    images=    ProductImage.objects.filter(variant=productt)
    print(productt.color)
    context = {
        'productt': productt,
        'variants': variants,
        'images':images,
    }
    return render(request, 'product_details.html', context)

def search(request):
    if request.method == "GET":
        query= request.GET.get('query')

        if  query:
            products = Product.objects.filter(name__icontains=query)
            if products:
             return render(request,'catagory.html', {'products': products})
            else:
             messages.info(request, 'No results found.')
    
        
            return redirect('cat','all')
     
    return render(request, 'catagory.html')



