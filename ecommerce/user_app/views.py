
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Category, CartItem
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from django.contrib.auth import authenticate, login, logout

def Register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken!'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('session_login')

    return render(request, 'register.html')

def session_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            request.session['username'] = user.username
            login(request, user)

            return redirect('session_dashboard')
        else:
            return render(request, 'login.html', {"error": "Invalid username or password"})

    return render(request, 'login.html')

# @login_required(login_url='session_login')
def session_dashboard(request):
    username = request.session.get('username')
    products = Product.objects.all()

    return render(request, 'dashboard.html', {
        'username': username,
        'products': products
    })


def session_logout(request):
    logout(request)
    return redirect('session_login')


# Helper to get session key (create one if not exists)
def _get_session_key(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key

# Product listing
def product_list(request):
    qs = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': qs, 'categories': categories})

# Product detail
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'user_app/product_detail.html', {'product': product})




# Add to cart (POST)

@login_required(login_url='session_login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("view_cart")



# View cart
@login_required(login_url='session_login')
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in items)

    return render(request, 'cart.html', {
        "cart_items": items,
        "cart_total": total
    })

# Update cart item quantity (POST)
@login_required(login_url='session_login')
def update_cart(request, cart_id):
    item = get_object_or_404(CartItem, id=cart_id, user=request.user)

    if request.method == "POST":
        qty = int(request.POST['quantity'])
        if qty > 0:
            item.quantity = qty
            item.save()

    return redirect("view_cart")


@login_required(login_url='session_login')
def remove_cart(request, cart_id):
    item = get_object_or_404(CartItem, id=cart_id, user=request.user)
    item.delete()
    return redirect("view_cart")


# Simple placeholder checkout
def checkout(request):
    # For demo: just clear the cart and show a success message
    if request.session.get('username'):
        try:
            user = User.objects.get(username=request.session['username'])
        except User.DoesNotExist:
            user = None
    else:
        user = None

    if user:
        CartItem.objects.filter(user=user).delete()
    else:
        session_key = _get_session_key(request)
        CartItem.objects.filter(session_key=session_key).delete()

    return render(request, 'checkout_success.html')






