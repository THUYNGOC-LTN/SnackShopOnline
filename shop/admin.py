from django.contrib import admin
from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    Category,
    Blog
)

# CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


# PRODUCT
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']


# ORDER
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'total_price',
        'status',
        'payment_method'
    ]


# ORDER ITEM
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'quantity'
    ]


# REVIEW
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'rating'
    ]


# CART
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


# CART ITEM
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'cart',
        'product',
        'quantity'
    ]


# BLOG
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Thông tin bài viết', {
            'fields': ('title', 'content', 'image')
        }),
        ('Tác giả', {
            'fields': ('author',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)