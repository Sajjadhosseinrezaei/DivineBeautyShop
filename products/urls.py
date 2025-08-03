from django.urls import path
from . import views




app_name = 'products'
urlpatterns = [
    path('list/', views.ProductListView.as_view(), name='product_lsit'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

]
