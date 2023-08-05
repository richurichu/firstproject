import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate,login,logout
from  django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from authenticate.tokens import account_activation_token
from django.contrib.sessions.backends.db import SessionStore
from cart.models import Cart
from userprofile.models import Wallet
from .models import *
from django.contrib.auth.hashers import make_password


from .models import otp_generation
import pyotp
from django.core.mail import send_mail





# @cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signup(request):
   
    if request.method == 'POST':
        username = request.POST['username']

        email = request.POST['email']
        pass1 = request.POST['password']
        cpassword = request.POST['cpassword']
        referral_code = request.POST['referral_code']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return render(request, 'signup.html', {'referral_code': referral_code})

        
       
        referrer = None
        if referral_code:
            try:
                referrer = User.objects.get(referral__referral_code=referral_code)
            except User.DoesNotExist:
                
                messages.error(request, 'Referral code is incorrect.')
                return render(request, 'signup.html', {'referral_code': referral_code})

    
        user = User(username=username, email=email)
        user.set_password(pass1)

       
        user.save()
        wallet = Wallet.objects.create(user=user)
        
        if referrer:
            Referral.objects.create(user=user, referral_code=generate_referral_code(), referred_by=referrer)
        else:
            Referral.objects.create(user=user, referral_code=generate_referral_code(), referred_by=None)
        
        # messages.success(request, 'your Account has been succesfully created')
        # senting activation link through mail
        current_site = get_current_site(request)
        subject = 'Activate Your plant Account'
        message = render_to_string('confirmEmail.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject,message)

        return render(request,'activation link.html')

    return render(request, 'signup.html')
def activate(request,uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

# @cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signin(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

       
        user = authenticate(username=username, password=password)
        

        if user is not None:
            
            otp_secret = pyotp.random_base32()

            # Create a PyOTP object
            totp = pyotp.TOTP(otp_secret)
           

            # Set the OTP expiration time (e.g., 5 minutes from the current time)
            # expiration_time = timezone.now() + datetime.timedelta(minutes=3)

            # Get the current OTP
            otp = totp.now()
           
            # Save the OTP to the user's OTP device
            # otp_device = otp_generation.objects.create(user=user, secret=totp, tokens=otp)
            # otp_device.token = otp
            
            # otp_device.expiration_time = expiration_time
            # otp_device.save()

            guest_session_key = request.session.session_key
            request.session['guest_session_key'] = guest_session_key 
            expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            session = SessionStore(request.session.session_key)
            request.session['otp'] = otp
            request.session['user_id'] = user.id
            request.session['otp_expiration_time'] = expiration_time.timestamp()

            # login(request, user)


            
               
               
                    
                    



            # Compose the email content
            subject = 'OTP verification'
            message = f'Hello {user.username},\n\n' \
                      f'Please use the following OTP to verify your email: {otp}\n\n' \
                      f'Thank you!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            return redirect('otp_login')


        else:
            messages.error(request, 'wrong username or password')
            return redirect('signin')

    return render(request, 'login.html')
       
  




# @cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.error(request, 'logedout successfully')
    return redirect('home')


def otp_login(request):

    if request.method == 'POST':
        otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
       
        user_id = request.session.get('user_id')
        expiration_time = request.session.get('otp_expiration_time')
     
        if session_otp == otp:
            if datetime.datetime.now().timestamp() < expiration_time:
                my_users = User.objects.get(id = user_id)
                login(request, my_users)

               
                guest_session_key = request.session.get('guest_session_key')
                # guest_session_key = request.session.get('session_key')
                guest_cart = Cart.objects.filter(session_key=guest_session_key).first()
               
                if guest_cart:
                    user_cart, created = Cart.objects.get_or_create(user=request.user)
                    

                    if not created:
                       for item in guest_cart.cartitems_set.all():
                          item.cart = user_cart
                          item.save()
                         
                
                
                    else:
                   
                         guest_cart.user = request.user
                         guest_cart.save()

               
                    user_cart.session_key = None
                    user_cart.save()



                    request.session['otp'] = None
                    request.session['user_id'] = None
                    request.session['session_key'] = None

                
                return redirect('home')
            else:
                request.session['otp'] = None
                request.session['user_id'] = None
                request.session['otp_expiration_time'] = None
                messages.error(request,'OTP has expired. Please request a new otp ')
        elif request.user.is_authenticated:
            # OTP is invalid, display an error message
            messages.error(request, 'Invalid OTP')
            messages.error(request, 'Invalid OTP.')

    
    messages.success(request, "we have sent an otp to your email")
    return render(request,'otp.html' )

def home(request):
    return render(request,'home.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        try:
           user = User.objects.get(username=username)
        except User.DoesNotExist:
           messages.error(request, 'username not matched ')
           return redirect('forgot_password')
        if user:
          if email == user.email:
            # Generate OTP secret
            otp_secret = pyotp.random_base32()

            # Create a PyOTP object
            totp = pyotp.TOTP(otp_secret)

            # Get the current OTP
            otp = totp.now()

            # setting timer
            expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

            # Store OTP in the session
            session = SessionStore(request.session.session_key)
            request.session['otp'] = otp
            request.session['user_id'] = user.id
            request.session['otp_expiration_time'] = expiration_time.timestamp()

            # Compose the email content
            subject = 'OTP verification'
            message = f'Hello {user.username},\n\n' \
                      f'Please use the following OTP to reset your password: {otp}\n\n' \
                      f'Thank you!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            return redirect('otp_forgot_password')
        
    return render(request, 'forgot_pass_1.html')


def otp_forgot_password(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        # Retrieve OTP from session
        session_otp = request.session.get('otp')
        user_id = request.session.get('user_id')
        expiration_time = request.session.get('otp_expiration_time')
        if session_otp == otp:
            if datetime.datetime.now().timestamp() < expiration_time:

                # Clear OTP from session
                request.session['otp'] = None
                

                return render(request, 'reset_password.html')

            else:
                # expired otp
                request.session['otp'] = None
                request.session['user_id'] = None
                request.session['otp_expiration_time'] = None
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('otp_login')

        elif request.user.is_active:
            # OTP is invalid, display an error message
            messages.error(request, 'Invalid OTP')

    # OTP verification not completed or authentication failed
    messages.success(request, "We have sent an OTP to your email.")
    return render(request, 'forgot_pass_2.html')


def reset_password(request):
   
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_id = request.session.get('user_id')
       
        if password1 == password2:
            user = User.objects.get(id=user_id)
            user.password = make_password(password2)
            user.save()
            request.session['user_id'] = None
            return redirect('signin')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('reset_password')

    return render(request, 'reset_password.html')

 