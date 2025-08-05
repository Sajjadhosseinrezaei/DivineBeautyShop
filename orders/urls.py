from django.urls import path, re_path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    re_path(r'cart/add/(?P<slug>[-\w]+)/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/update/<int:cart_item_id>/', views.CartUpdateView.as_view(), name='cart_update'),
    path('cart/remove/<int:cart_item_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
]
