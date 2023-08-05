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
    path('Return_orderss/<int:order_id>/',views.Return_orderss, name='Return_orderss'),
    path('initiate_payment',views.initiate_payment, name='initiate_payment'),
    path('online_payment_order/<int:add_id>/',views.online_payment_order,name='online_payment_order'),
    # path('invoice_download/<int:order_id>/',views.invoice_download, name='invoice_download'),
    path('invoice_download_start/<int:order_id>/',views.invoice_download_start, name='invoice_download_start'),
     


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)