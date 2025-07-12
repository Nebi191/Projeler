from django.contrib.auth import views as auth_views # type: ignore
from django.urls import path  # type: ignore
from . import views
app_name = 'store'

urlpatterns = [
    path('',views.home,name='home'),
    path('index/',views.index,name='index'),
    path('home/', views.home,name='home'),
    path('about/',views.about,name='about'),
    path('new/',views.new,name='new'),
    path('populer/',views.populer,name='populer'),
    path('register/',views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('cart/',views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('items/',views.items, name='items'),
    path('cart/remove/<int:product_id>/',views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path("payment/", views.payment_request, name="payment"),
    path('shipping_address/',views.shipping_address_view,name='shipping_address'),
    path('create-order/', views.create_order, name='create_order'),
    path('create-order/', views.create_order, name='create_order'),
    path('success/',views.success,name='success'),
    path('create-order/<int:shipping_id>/', views.create_order, name='create_order'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('order-history/',views.order_history, name='order_history')
    # path('order_summary/<int:order_id>/',views.order_summary,name='order_summary'),
    # path('payment/callback/', views.payment_callback, name='payment_callback')

    
    
]
