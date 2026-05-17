from django.db import models
from django.contrib.auth.models import User
import uuid

# CATEGORY
class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# USER PROFILE
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Profile - {self.user.username}"


# PRODUCT
class Product(models.Model):

    name = models.CharField(max_length=200)

    price = models.IntegerField()

    image = models.ImageField(upload_to='products/')

    description = models.TextField()
    sold_count = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

# =========================
# CART
# =========================
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Cart - {self.user.username}"


# =========================
# CART ITEM
# =========================
class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# =========================
# ORDER
# =========================
class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Chờ xác nhận'),
        ('CONFIRMED', 'Đã xác nhận'),
        ('SHIPPING', 'Đang giao'),
        ('DELIVERED', 'Đã giao'),
        ('CANCELLED', 'Đã hủy'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng'),
        ('BANKING', 'Chuyển khoản'),
    ]

    PAYMENT_STATUS = [
        ('UNPAID', 'Chưa thanh toán'),
        ('PENDING', 'Chờ thanh toán'),
        ('PAID', 'Đã thanh toán'),
        ('FAILED', 'Thanh toán thất bại'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order_code = models.CharField(max_length=20, unique=True, blank=True)

    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    total_price = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='UNPAID'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = "OD" + uuid.uuid4().hex[:8].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_code

# =========================
# ORDER ITEM
# =========================
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    price = models.FloatField(default=0)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# =========================
# REVIEW
# =========================
class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()  # 1 -> 5 sao

    comment = models.TextField()

    image = models.ImageField(
        upload_to='reviews/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# =========================
# BLOG
# =========================
class Blog(models.Model):
    title = models.CharField(max_length=300)
    
    content = models.TextField()
    
    image = models.ImageField(upload_to='blogs/')
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# =========================
# SHOP REVIEW
# =========================
class ShopReview(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    rating = models.IntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Payment(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Chờ thanh toán'),
        ('PAID', 'Đã thanh toán'),
        ('FAILED', 'Thất bại'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.PositiveIntegerField()

    transaction_code = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)