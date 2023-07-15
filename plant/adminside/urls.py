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



]