from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  
      path('view_cart',views.view_cart,name='view_cart'),
      path('add_to_cart/<int:variant_id>/',views.add_to_cart,name='add_to_cart'),
      path('update_quantity', views.update_quantity, name='update_quantity'),
      path('remove_from_cart',views.remove_from_cart,name='remove_from_cart'),
      path('apply_coupon',views.apply_coupon,name='apply_coupon'),
      path('add_to_whishlist/<int:variant_id>/',views.add_to_whishlist,name='add_to_whishlist'),
      path('remove_wish/<int:variant_id>/',views.remove_wish,name='remove_wish'),
      path('view_wishlist',views. view_wishlist,name='view_wishlist'),
  


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)