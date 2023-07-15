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
     
  


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)