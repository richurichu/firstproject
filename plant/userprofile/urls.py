from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
      path('profile_view',views.profile_view,name='profile_view'),
      path('add_address',views.add_address,name='add_address'),
      path('show_address',views.show_address,name='show_address'),
      path('edit_address/<int:address_id>',views.edit_address,name='edit_address'),
      path('order_address',views.order_address,name='order_address'),
  


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)