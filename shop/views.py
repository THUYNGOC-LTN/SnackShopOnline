from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Avg, Count, Q, Max
from datetime import timedelta
from django.utils import timezone
from .models import ShopReview
from django.http import JsonResponse

from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, UserProfile, Blog
from .forms import ProductForm, UserProfileForm, UserProfilePictureForm, ReviewForm, BlogForm

# =========================
# HOME + SEARCH
# =========================
def home(request):

    # ADMIN -> dashboard riêng
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    q = request.GET.get('q')

    # PRODUCTS
    products = Product.objects.all().order_by('-id')

    # CATEGORY
    categories = Category.objects.all()

    # SEARCH
    if q:
        products = products.filter(
            name__icontains=q
        )

    # BEST SELLERS
    best_sellers = Product.objects.annotate(
        total_sold=Count('orderitem')
    ).filter(
        total_sold__gt=0
    ).order_by('-total_sold')[:4]

    # NEW PRODUCTS
    new_products = Product.objects.all().order_by('-id')[:4]

    # SHOP REVIEWS
    shop_reviews = ShopReview.objects.all().order_by('-id')[:20]

    # CART COUNT
    cart_count = get_cart_count(request.user)

    return render(request, 'shop/home.html', {

        'products': products,

        'categories': categories,

        'selected_category': None,

        'best_sellers': best_sellers,

        'new_products': new_products,

        'shop_reviews': shop_reviews,

        'cart_count': cart_count

    })
# =========================
# REGISTER
# =========================
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # 👈 thêm dòng này

        # CHECK mật khẩu không khớp
        if password != confirm_password:
            return render(request, 'auth/register.html', {
                'error': 'Mật khẩu không khớp'
            })

        # CHECK username tồn tại
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {
                'error': 'Username đã tồn tại'
            })

        # Tạo user
        User.objects.create_user(username=username, password=password)

        return redirect('login')

    return render(request, 'auth/register.html')

# =========================
# LOGIN
# =========================
def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')

        return render(request, 'auth/login.html', {
            'error': 'Sai tài khoản hoặc mật khẩu'
        })

    return render(request, 'auth/login.html')


# =========================
# LOGOUT
# =========================
def user_logout(request):
    logout(request)
    return redirect('login')


# =========================
# ADD TO CART
# =========================
@login_required
def add_to_cart(request, product_id):

    # ADMIN không được mua hàng
    if request.user.is_staff:
        return redirect('admin_dashboard')

    # Lấy sản phẩm
    product = get_object_or_404(
        Product,
        id=product_id
    )

    # Tạo giỏ hàng
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # Kiểm tra sản phẩm đã có chưa
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # Nếu đã có -> tăng số lượng
    if not created:
        item.quantity += 1
        item.save()

    return redirect('home')


# =========================
# VIEW CART
# =========================
@login_required
def view_cart(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)
    total_items = sum(item.quantity for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total,
        'total_items': total_items
    })


# =========================
# UPDATE QUANTITY
# =========================
@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])

        if quantity > 0:
            item.quantity = quantity
            item.save()

    return redirect('cart')


# =========================
# REMOVE ITEM
# =========================
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


# =========================
# CHECKOUT
# =========================
@login_required
def checkout(request):

    # ADMIN không được checkout
    if request.user.is_staff:
        return redirect('admin_dashboard')

    # Lấy giỏ hàng
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = CartItem.objects.filter(
        cart=cart
    )

    # Không có sản phẩm
    if not items.exists():
        return redirect('home')

    # =========================
    # TÍNH TỔNG TIỀN
    # =========================
    total = 0

    for item in items:

        total += (
            item.product.price *
            item.quantity
        )

    # =========================
    # ĐẶT HÀNG
    # =========================
    if request.method == 'POST':

        fullname = request.POST.get(
            'fullname'
        )

        phone = request.POST.get(
            'phone'
        )

        address = request.POST.get(
            'address'
        )

        payment_method = request.POST.get(
            'payment_method',
            'COD'
        )

        # VALIDATE
        if not fullname or not phone or not address:

            messages.error(
                request,
                "Vui lòng nhập đầy đủ thông tin"
            )

            return redirect('checkout')

        # =========================
        # TẠO ORDER
        # =========================
        order = Order.objects.create(

            user=request.user,

            fullname=fullname,

            phone=phone,

            address=address,

            total_price=total,

            payment_method=payment_method,

            status='PENDING'

        )

        # =========================
        # TẠO ORDER ITEMS
        # =========================
        for item in items:

            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price

            )
        # =========================
        # TĂNG SỐ LƯỢNG ĐÃ BÁN
        # =========================
        for item in items:
            product = item.product
            product.sold_count += item.quantity

        for item in items:
            item.product.save()

        # =========================
        # XÓA GIỎ HÀNG
        # =========================
        items.delete()

        # =========================
        # BANKING
        # =========================
        if payment_method == 'BANKING':

            return redirect(
                'payment_qr',
                order_id=order.id
            )

        # =========================
        # COD
        # =========================
        return redirect(
            'order_success',
            order_code=order.order_code
        )

    # =========================
    # HIỂN THỊ CHECKOUT
    # =========================
    return render(
        request,
        'shop/checkout.html',
        {
            'items': items,
            'total': total
        }
    )


# =========================
# HELPER: CART COUNT
# =========================
def get_cart_count(user):

    if user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=user
        )

        items = CartItem.objects.filter(
            cart=cart
        )

        return sum(
            item.quantity
            for item in items
        )

    return 0


# =========================
# BLOG
# =========================
def blog_list(request):
    """Hiển thị danh sách các bài viết blog"""
    blogs = Blog.objects.all()
    
    return render(request, 'blog/list.html', {
        'blogs': blogs,
        'cart_count': get_cart_count(request.user)
    })


def blog_detail(request, blog_id):
    """Hiển thị chi tiết bài viết blog"""
    blog = get_object_or_404(Blog, id=blog_id)
    
    return render(request, 'blog/detail.html', {
        'blog': blog,
        'cart_count': get_cart_count(request.user)
    })


@login_required(login_url='login')
def create_blog(request):
    """Admin tạo bài viết blog"""
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, '✅ Bài viết được đăng thành công!')
            return redirect('blog_list')
    else:
        form = BlogForm()
    
    return render(request, 'blog/create.html', {
        'form': form,
        'cart_count': get_cart_count(request.user)
    })


@login_required(login_url='login')
def edit_blog(request, blog_id):
    """Admin chỉnh sửa bài viết blog"""
    blog = get_object_or_404(Blog, id=blog_id)
    
    if blog.author != request.user and not request.user.is_superuser:
        return redirect('blog_list')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Bài viết được cập nhật thành công!')
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'blog/edit_blog.html', {
        'form': form,
        'blog': blog,
        'cart_count': get_cart_count(request.user)
    })


@login_required(login_url='login')
def delete_blog(request, blog_id):
    """Admin xóa bài viết blog"""
    blog = get_object_or_404(Blog, id=blog_id)
    
    if blog.author != request.user and not request.user.is_superuser:
        return redirect('blog_list')
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, '✅ Bài viết được xóa thành công!')
        return redirect('blog_list')
    
    return render(request, 'blog/delete_blog.html', {
        'blog': blog,
        'cart_count': get_cart_count(request.user)
    })

# =========================
# ORDER SUCCESS
# =========================
def order_success(request, order_code):

    order = Order.objects.get(order_code=order_code)

    return render(request, "orders/success.html", {
        "order": order
    })

# =========================
# ORDER HISTORY
# =========================
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders/list.html', {'orders': orders})


# =========================
# ORDER DETAIL
# =========================
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    return render(request, 'orders/detail.html', {
        'order': order,
        'items': items
    })


# =========================
# USER PROFILE
# =========================
@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    return render(request, 'auth/profile.html', {
        'user': user,
        'user_profile': user_profile,
        'orders': orders
    })


# =========================
# EDIT USER PROFILE
# =========================
@login_required
def edit_profile(request):
    # Get or create UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        avatar_form = UserProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and avatar_form.is_valid():
            user_form.save()
            avatar_form.save()
            messages.success(request, 'Cập nhật hồ sơ thành công!')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        avatar_form = UserProfilePictureForm(instance=user_profile)
    
    return render(request, 'auth/edit_profile.html', {
        'form': user_form,
        'avatar_form': avatar_form
    })

# =========================
# CATEGORY PRODUCTS 
def category_products(request, category_id):

    categories = Category.objects.all()

    selected_category = get_object_or_404(
        Category,
        id=category_id
    )

    products = Product.objects.filter(
        category=selected_category
    )

    cart_count = get_cart_count(request.user)

    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'cart_count': cart_count
    })

# =========================
# ALL PRODUCTS
# =========================
def all_products(request):
    
    # ADMIN -> dashboard riêng
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    q = request.GET.get('q')
    sort = request.GET.get('sort', '-id')
    category_id = request.GET.get('category')
    
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = None
    
    # FILTER by category
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=selected_category)
    
    # SEARCH
    if q:
        products = products.filter(name__icontains=q)
    
    # SORT
    if sort == 'best_seller':
        products = products.annotate(total_sold=Count('orderitem')).order_by('-total_sold')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by(sort)
    
    cart_count = get_cart_count(request.user)
    
    return render(request, 'shop/products.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'cart_count': cart_count,
        'sort': sort,
        'q': q
    })

# =========================
# PRODUCT DETAIL
# =========================
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    
    can_review = False
    if request.user.is_authenticated:
        can_review = OrderItem.objects.filter(
            order__user=request.user,
            product=product
        ).exists()

    return render(request, 'shop/detail.html', {
        'product': product,
        'reviews': reviews,
        'can_review': can_review,
        'avg_rating': avg_rating,
    })


# =========================
# ADD REVIEW
# =========================
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    has_bought = OrderItem.objects.filter(
        order__user=request.user,
        product=product
    ).exists()

    if not has_bought:
        messages.error(request, "Bạn cần mua sản phẩm trước khi đánh giá")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "🎉 Đánh giá thành công!")
        else:
            messages.error(request, "Có lỗi khi tạo đánh giá")

    return redirect('product_detail', product_id=product.id)


# =========================
# PAYMENT QR
# =========================
@login_required
def payment_qr(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'orders/payment_qr.html', {
        'order': order
    })


# =========================
# CONFIRM PAYMENT
# =========================
@login_required
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    order.status = 'CONFIRMED'
    order.save()

    return redirect('orders')


# =========================
# CANCEL ORDER
# =========================
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['PENDING', 'CONFIRMED']:
        order.status = 'CANCELLED'
        order.save()

    return redirect('orders')


# =========================
# ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('home')

    # THỐNG KÊ
    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_users = User.objects.count()

    total_blogs = Blog.objects.count()

    revenue = sum(
    float(order.total_price)
    for order in Order.objects.all()
    )

    # ĐƠN HÀNG MỚI
    recent_orders = Order.objects.all().order_by(
        '-created_at'
    )

    # BÀI BLOG MỚI
    recent_blogs = Blog.objects.all().order_by('-created_at')[:5]

    # FORM THÊM SẢN PHẨM
    form = ProductForm()

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            return redirect(
                'admin_dashboard'
            )

    # DANH SÁCH SẢN PHẨM
    products = Product.objects.all().order_by('-id')[:8] 
    orders = Order.objects.all().order_by('-id')

    return render(
        request,
        'admin/dashboard.html',
        {

            'total_products': total_products,

            'total_orders': total_orders,

            'total_users': total_users,

            'total_blogs': total_blogs,

            'revenue': revenue,

            'recent_orders': recent_orders,

            'recent_blogs': recent_blogs,

            'form': form,

            'products': products,
            'orders': orders,

        }
    )
 
# ========================= 
# UPDATE STATUS (ADMIN)
# =========================
@login_required
def update_order_status(request, order_id):

    if not request.user.is_staff:
        return redirect('home')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == 'POST':

        order.status = request.POST.get(
            'status'
        )

        order.save()

    return redirect('admin_dashboard') 

# =========================
# DELETE PRODUCT
# =========================
@login_required
def delete_product(request, id):

    if not request.user.is_staff:
        return redirect('home')

    product = get_object_or_404(
        Product,
        id=id
    )

    product.delete()

    return redirect('admin_dashboard')

# =========================
# DELETE ORDER (ADMIN)
# =========================
@login_required
def delete_order(request, id):

    if not request.user.is_staff:
        return redirect('home')

    order = get_object_or_404(
        Order,
        id=id
    )

    order.delete()

    return redirect('admin_dashboard')

# =========================
# EDIT PRODUCT
# =========================
@login_required
def edit_product(request, id):

    if not request.user.is_staff:
        return redirect('home')

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect(
                'admin_dashboard'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(request, 'shop/edit_product.html', {
        'form': form,
        'product': product
    })

# =========================
# INCREASE CART QUANTITY
# =========================
@login_required
def increase_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.quantity += 1

    item.save()

    return redirect('cart')

# =========================
# DECREASE CART QUANTITY
@login_required
def decrease_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    else:

        item.delete()

    return redirect('cart')

@login_required
def add_shop_review(request):

    if request.method == "POST":

        rating = request.POST.get("rating")
        message = request.POST.get("message")

        review = ShopReview.objects.create(
            user=request.user,
            rating=rating,
            message=message
        )

        return JsonResponse({
            "success": True,
            "username": review.user.username,
            "rating": review.rating,
            "message": review.message
        })

    return JsonResponse({
        "success": False
    })