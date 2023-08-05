from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

from authenticate.models import Referral
from .models import *
from django.contrib import messages

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
        return redirect('add_address')
   
     return render(request ,'show_address.html', {'addresses': addresses} )

                                                                                                        
def order_address(request):
  if request.user.is_authenticated:
   
     user = request.user
     try:
        addresses = User_address.objects.filter(user=user)
        if not addresses.exists():
            # If the user has no addresses, redirect to the 'add_address' view
            
            return redirect('no_adress_add')
     except ObjectDoesNotExist:
        # Handle the exception if any other unexpected error occurs
        return HttpResponse('Something went wrong.')
     
     return render(request ,'orderaddress.html', {'addresses': addresses} )
  else:
      return redirect('signin')
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
        return redirect('show_address')
    return render(request,'add_address.html')


def no_adress_add(request):
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
        return redirect('order_address')
    return render(request,'no_address.html')


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
        return redirect('show_address')
     context = {
         'user_address':user_address,
         'address_id':address_id,
     }
     return render(request,'edit_address.html',context)


def order_edit_address(request,address_id):
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
        return redirect('order_address')
     context = {
         'user_address':user_address,
         'address_id':address_id,
     }
     return render(request,'order_edit_address.html',context)

def delete_address(request,address_id):
     try:
        user_address = User_address.objects.get(id=address_id, user=request.user)
        user_address.delete()
       
     except User_address.DoesNotExist:
        return HttpResponse('Address not found.')
     return redirect('show_address')


def refer(request):
    user = request.user
    try:
        referral = Referral.objects.get(user=user)
    except Referral.DoesNotExist:
        referral = None

    return render(request,'refer_offer.html',{'user': user, 'referral': referral})

def wallet(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        wallet = None
    
    try:
        addresses = User_address.objects.filter(user=user)
    except ObjectDoesNotExist:
      
        addresses = None
    context={
        'wallet':wallet,
        'addresses':addresses
    }

    return render(request,'wallet.html', context)


def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if request.user.is_authenticated:
            user = request.user

           
            if not check_password(old_password, user.password):
                messages.error(request, 'Old password is incorrect.')
                return redirect('change_password')

            if password1 == password2:
                user.password = make_password(password2)
                user.save()
                return render(request,'user_profile.html')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('change_password')
        else:
            messages.error(request, 'User not authenticated.')
            return redirect('change_password')

    return render(request, 'change_password.html')