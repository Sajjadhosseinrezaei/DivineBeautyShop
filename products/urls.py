from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('list/', views.ProductListView.as_view(), name='product_list'),
    path('list/<int:id>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
