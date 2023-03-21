from django.urls import path
from . import views

urlpatterns = [
    path('product/<str:id>', views.product, name="product"),
    path('add-to-cart/<str:id>', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
    path('cart/plus-quantity/', views.plus_quantity, name="plus_quantity"),
    path('cart/minus-quantity/', views.minus_quantity, name="minus_quantity"),
    path('cart/remove-cart/', views.removeCart, name="removeCart"),
    path('payment/', views.sslcommerz_payment, name="payment"),
    path('payment/success/', views.sslcommerz_success, name="success"),
    path('payment/fail/', views.sslcommerz_fail, name="fail"),
]

