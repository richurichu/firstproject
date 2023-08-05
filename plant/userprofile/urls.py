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
      path('order_edit_address/<int:address_id>',views.order_edit_address,name='order_edit_address'),
      path('order_address',views.order_address,name='order_address'),
      path('delete_address/<int:address_id>',views.delete_address,name='delete_address'),
      path('refer',views.refer,name='refer'),
      path('wallet',views.wallet,name='wallet'),
      path('change_password',views.change_password,name='change_password'),
      path('no_adress_add',views.no_adress_add,name='no_adress_add'),
  



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)