from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
    path('checkout/<int:add_id>/',views.checkout,name='checkout'),
    path('placeorder/<int:add_id>/',views.placeorder,name='placeorder'),
    
    path('orders',views.orders, name='orders'),
    path('order-view/<int:order_id>/',views.order_view, name='order_view'),
    path('cancel_orderss/<int:order_id>/',views.cancel_orderss, name='cancel_orderss'),
     
     


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)