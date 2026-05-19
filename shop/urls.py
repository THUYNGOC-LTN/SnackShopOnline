from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete-order/<int:id>/', views.delete_order, name='delete_order'),
    path(
    'payment-qr/<str:order_code>/',
    views.payment_qr,
    name='payment_qr'
    ),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('order-success/<str:order_code>/',views.order_success, name='order_success'), 
    path('update-order-status/<int:order_id>/',views.update_order_status, name='update_order_status'), 
    path('increase-cart/<int:item_id>/',views.increase_cart,name='increase_cart'),
    path('decrease-cart/<int:item_id>/',views.decrease_cart,name='decrease_cart'),
    path('category/<int:id>/',views.category_products, name='category_products'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('products/', views.all_products, name='all_products'),
    path(
    'shop-review/',
    views.add_shop_review,
    name='add_shop_review'
    ),
    path('webhook/payment/', views.payment_webhook, name='payment_webhook'),
    path(
    'check-payment/<str:order_code>/',
    views.check_payment,
    name='check_payment'
    ),
]