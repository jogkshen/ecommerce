from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, OrderForm
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse

def index (request):
    return render (request, 'index.html')

def home(request):
    cat_name = "trending"
    m_name ="mens fashion"

    categories = Category.objects.all()
    products = Product.objects.all()
    mcategory = Category.objects.get(name=m_name)
    fmen = Product.objects.filter(category = mcategory)

    tcategory = Category.objects.get(name=cat_name)
    trending = Product.objects.filter(category = tcategory)

    #p = Product.objects.filter(category = 'ketako')
    latest_products = Product.objects.all().order_by('-id')[:4]
    today = TodayDeal.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'categories': categories, 'products': products, 
                                         'latest_products': latest_products, 'today': today, 
                                         'trending': trending, 'fmen': fmen})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')  
        else:
            # Display form errors in the template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:

            login(request, user)
            
            return redirect('home')
        else:
    
            messages.error(request, 'Login failed. Please check your credentials.')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def trending(request):
    cat_name = "trending"
    tcategory = Category.objects.get(name=cat_name)
    trending = Product.objects.filter(category = tcategory)
    return render(request, 'trending.html', {'trending': trending})

def mens(request):
    cat_name = "mens fashion"
    tcategory = Category.objects.get(name=cat_name)
    trending = Product.objects.filter(category = tcategory)
    return render(request, 'mensfashion.html', {'trending': trending})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.is_authenticated:
        # Get or create the user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        # Add the product to the user's cart
        user_cart.products.add(product)

        messages.success(request, f"{product.title} has been added to your cart!")
        return redirect('cart_list')
    else:
        messages.warning(request, "Please log in to add items to your cart.")
        return redirect('login') 
    

def add_order(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                form.instance.product = product
                form.instance.user = request.user
                form.save()
                success_message = f"Your order for {product.title} has been placed successfully!"
                return redirect('success', success_message=success_message) 
            else:
                messages.error(request, "There was an error processing your order. Please check your inputs.")
        else:
            form = OrderForm(initial={'product': product})
        return render(request, 'order.html', {'form': form})
    else:
        messages.warning(request, "Please log in to place an order.")
        return redirect('login')  # Redirect to the login page if the user is not authenticated


    
@login_required
def cart_list(request):
    # Retrieve the user's cart from the database
    user_cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'cart_list.html', {'user_cart': user_cart})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def search_product(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'search_result.html', {'products': products})


def success(request, success_message):
    return render(request, 'success.html', {'success_message': success_message})

