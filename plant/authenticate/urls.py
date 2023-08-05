from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('',views.home,name='home'),
    path('signout',views.signout,name='signout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # path('verification-mail-sent/',views.verification_mail_sent,name='verification_mail_sent'),
    path('otp_login',views.otp_login,name='otp_login'),

    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('otp_forgot_password',views.otp_forgot_password,name='otp_forgot_password'),
    path('reset_password',views.reset_password,name='reset_password'),


]
