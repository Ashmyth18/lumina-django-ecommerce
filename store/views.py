from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem


def home(request):
    featured = Product.objects.filter(featured=True, stock__gt=0)[:6]
    categories = Category.objects.all()[:8]
    latest = Product.objects.filter(stock__gt=0)[:8]
    return render(request, 'store/home.html', {
        'featured': featured,
        'categories': categories,
        'latest': latest,
    })


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()

    q = request.GET.get('q', '')
    cat_slug = request.GET.get('category', '')
    sort = request.GET.get('sort', '-created_at')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    sort_options = {
        'price_asc': 'price', 'price_desc': '-price',
        'name': 'name', '-created_at': '-created_at',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'selected_category': cat_slug,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address', '')
        order = Order.objects.create(user=request.user, shipping_address=address)
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order, product=item.product,
                quantity=item.quantity, price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
        order.calculate_total()
        cart.cart_items.all().delete()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_detail', order_id=order.id)

    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
