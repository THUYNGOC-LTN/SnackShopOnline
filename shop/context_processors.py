from .models import Cart, CartItem


def cart_count(request):
    """Add cart count to every template context"""
    cart_count_value = 0
    
    if request.user.is_authenticated and not request.user.is_staff:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            # Sum all quantities instead of counting items
            cart_count_value = sum(
                item.quantity for item in CartItem.objects.filter(cart=cart)
            )
    
    return {
        'cart_count': cart_count_value
    }
