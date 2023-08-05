from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from store import models




urlpatterns = [
  
    path('admins',views.admins,name='admins'),
    path('customers',views.customers,name='customers'),
    path('block-user/<int:id>/',views.block_user,name='block_user'),
    path('unblock-user/<int:id>/',views.unblock_user,name='unblock_user'),

    path('admin_catagory',views.admin_catagory,name='admin_catagory'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('add-category',views.add_category,name='add_category'),
    path('disable-category/<int:id>/',views.disable_category,name='disable_category'),
    path('enable-category/<int:id>/',views.enable_category,name='enable_category'),

    path('admin-products',views.admin_products,name='admin_products'),
    path('admin-varients/<int:id>/',views.admin_varients,name='admin_varients'),
    path('admin-addvarients/<int:id>/',views.admin_addvarients,name='admin_addvarients'),
    path('admin_addproduct',views.admin_addproduct,name='admin_addproduct'),
    path('admin-editvarients/<int:id>/',views.admin_editvarients,name='admin_editvarients'),
    path('admin-disablevarients/<int:id>/',views.admin_disablevarients,name='admin_disablevarients'),
    path('admin-enablevarients/<int:id>/',views.admin_enablevarients,name='admin_enablevarients'),

    path('admin_orders', views.admin_orders, name='admin_orders'),
    path('order_views/<int:order_id>',views.order_views,name='order_views'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order_complete/<int:order_id>/', views.order_complete, name='order_complete'),

    path('shipped/<int:order_id>/', views.shipped, name='shipped'),

    path('view_coupon', views.view_coupon, name='view_coupon'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('disable_coupon/<int:coupon_id>/', views.disable_coupon, name='disable_coupon'),
    path('enable_coupon/<int:coupon_id>/', views.enable_coupon, name='enable_coupon'),
    path('add_coupon', views.add_coupon, name='add_coupon'),
    path('admin_view_referral', views.admin_view_referral, name='admin_view_referral'),
    path('edit_referral_program', views.edit_referral_program, name='edit_referral_program'),
    # path('add_new_referral_offer', views.add_new_referral_offer, name='add_new_referral_offer'),
    path('add_banner', views.add_banner, name='add_banner'),
    path('list_banners', views.list_banners, name='list_banners'),
    path('delete_banner/<int:banner_id>/', views.delete_banner, name='delete_banner'),
    path('edit_banner/<int:banner_id>/', views.edit_banner, name='edit_banner'),

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),

    path('pdf_view', views.pdf_view, name = 'pdf_view'),
    path('download_order_pdf_sales', views.download_order_pdf_sales, name = 'download_order_pdf_sales'),
    path('add_colour', views.add_colour, name = 'add_colour'),
    

]