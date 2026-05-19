from .models import Cart, CartItem


def cart_count(request):
    """Add cart count to every template context"""
    cart_count_value = 0
    
    if request.user.is_authenticated and not request.user.is_staff:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count_value = CartItem.objects.filter(cart=cart).count()
    
    return {
        'cart_count': cart_count_value
    }
