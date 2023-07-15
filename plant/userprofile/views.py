from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def profile_view(request):
    user = request.user
    try:
        addresses = User_address.objects.filter(user=user)
    except ObjectDoesNotExist:
      
        addresses = None
   
    return render(request ,'user_profile.html', {'addresses':addresses} )

def show_address(request):
   
     user = request.user
     try:
        addresses = User_address.objects.filter(user=user)
     except ObjectDoesNotExist:
      
        addresses = None
   
     return render(request ,'show_address.html', {'addresses': addresses} )

                                                                                                        
def order_address(request):
   
     user = request.user
     try:
        addresses = User_address.objects.filter(user=user)
     except ObjectDoesNotExist:
      
        addresses = None
   
     return render(request ,'orderaddress.html', {'addresses': addresses} )

def add_address(request):
    if request.method == 'POST':
        
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        address_line_1 = request.POST['address1']
        address_line_2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['pincode']
        country = request.POST['country']
        email = request.POST['email']
        phone_number = request.POST['phone']

        
        address = User_address(
            user=request.user,  # Assuming the request has a logged-in user
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            email=email,
            phone_number=phone_number
        )
        address.save()
        return redirect('profile_view')
    return render(request,'add_address.html')

def edit_address(request,address_id):
     try:
        user_address = User_address.objects.get(id=address_id, user=request.user)
     except User_address.DoesNotExist:
        return HttpResponse('Address not found.')
     
     if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        address_line_1 = request.POST['address1']
        address_line_2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['pincode']
        country = request.POST['country']
        email = request.POST['email']
        phone_number = request.POST['phone']


        # Update the user address fields
        user_address.first_name = first_name
        user_address.last_name = last_name
        user_address.address_line_1 = address_line_1
        user_address.address_line_2 = address_line_2
        user_address.city = city
        user_address.state = state
        user_address.postal_code = postal_code
        user_address.country = country
        user_address.email = email
        user_address.phone_number = phone_number

        # Save the updated user address
      
        user_address.save()
        return redirect('profile_view')
     context = {
         'user_address':user_address,
         'address_id':address_id,
     }
     return render(request,'edit_address.html',context)
