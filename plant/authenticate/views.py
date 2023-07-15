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


from .models import otp_generation
import pyotp
from django.core.mail import send_mail





# @cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']

        email = request.POST['email']
        pass1 = request.POST['password']
        cpassword = request.POST['cpassword']
        user = User.objects.create_user(username=username, email=email, password=pass1)

        user.save()
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
            print('totp =====',totp)

            # Set the OTP expiration time (e.g., 5 minutes from the current time)
            # expiration_time = timezone.now() + datetime.timedelta(minutes=3)

            # Get the current OTP
            otp = totp.now()
            print('otp',otp)
            # Save the OTP to the user's OTP device
            otp_device = otp_generation.objects.create(user=user, secret=totp, tokens=otp)
            otp_device.token = otp
            print(".....................",otp_device.token)
            # otp_device.expiration_time = expiration_time
            otp_device.save()

            login(request, user)

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
        otp_device = otp_generation.objects.get(user=request.user)
        print('otp_device:', otp_device)
        print(otp_device.tokens)
        print(request.user)

        # if otp_device.expiration_time < timezone.now():
        #     # OTP has expired
        #     messages.error(request, 'OTP has expired. Please request a new one.')

        if otp_device.tokens == str(otp):

            # Delete the OTP device after verification
            otp_device.delete()

            return redirect('home')

        else:
            # OTP is invalid, display an error message
            
            messages.error(request, 'Invalid OTP.')
    messages.success(request, "we have sent an otp to your email")
    return render(request,'otp.html')

def home(request):
    return render(request,'home.html')