from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
  
    path('',views.home,name='home'),
    path('cat/<slug:slug>/',views.cat,name='cat'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search',views.search,name='search'),
  


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)