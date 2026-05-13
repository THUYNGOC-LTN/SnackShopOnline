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

    PAYMENT_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng'),
        ('BANKING', 'Chuyển khoản'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Mã đơn hàng
    order_code = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    # Thông tin người nhận
    fullname = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    address = models.TextField()

    # Tổng tiền
    total_price = models.PositiveIntegerField(default=0)

    # Trạng thái
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    # Thanh toán
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    # Thời gian đặt
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        # Tạo mã đơn tự động
        if not self.order_code:
            self.order_code = "OD" + str(uuid.uuid4().hex[:8]).upper()

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
