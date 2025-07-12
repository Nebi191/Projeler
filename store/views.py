import json
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from . import views
from .models import Product, ShippingAddress, Order, OrderItem
from django.contrib.auth import login, authenticate, logout # type: ignore
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm # type: ignore
from django.contrib import messages # type: ignore
import iyzipay # type: ignore
from .forms import ShippingAddressForm
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.http import HttpResponse # type: ignore
from django.conf import settings # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .models import Order


# Create your views here.


def index(request):
    return render(request,'store/index.html')

def home(request):
    products = Product.objects.all()
    return render(request,'store/home.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')

def new(request):
    products = Product.objects.filter(is_new=True)
    return render(request,'store/new.html', {'products':products})

def populer(request):
    products = Product.objects.filter(is_popular=True)
    return render(request,'store/populer.html', {'products':products})

def success(request):
    return render(request, 'store/success.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz")
            return redirect('store:login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hoş geldiniz {user.username}!")
                return redirect('store:home')
            else:
                messages.error(request, "Geçersiz kullanıcı adı veya şifre")
        else:
            messages.error(request, "Form doğrulanamadı")
    else:
        form = AuthenticationForm()
    
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect('store:home')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] =1

    request.session['cart'] = cart

    messages.success(request, f"{product.name} sepete eklendi.")
    return redirect('store:cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {'cart_items': products, 'total': total})


def items(request):
    products = Product.objects.all()
    return render(request,'store/items.html', {'products':products})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, "Ürün sepetten çıkarıldı.")
    else:
        messages.error(request, "Ürün sepetinizde bulunamadı.")
    
    return redirect('store:cart')

def clear_cart(request):
    request.session['cart'] = {}
    messages.success(request, "Sepetiniz boşaltıldı")
    return redirect('store:cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
        messages.success(request, "Ürün miktarı artırıldı.")
    else:
        messages.error(request, "Ürün sepette bulunamadı.")
    request.session['cart'] = cart
    return redirect('store:cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
            messages.success(request, "Ürün miktarı azaltıldı.")
        else:

            del cart[str(product_id)]
            messages.success(request, "Ürün sepetten çıkarıldı.")
    else:
        messages.error(request, "Ürün sepette bulunamadı.")

    request.session['cart'] = cart
    return redirect('store:cart')
    




def payment_request(request):
    options = {
        "api_key": settings.IYZICO_API_KEY,
        "secret_key": settings.IYZICO_SECRET_KEY,
        "base_url": settings.IYZICO_BASE_URL
    }

    basket_items = [
        {
            "id": "BI101",
            "name": "Örnek Ürün",
            "category1": "Kategori",
            "itemType": "PHYSICAL",
            "price": "10"
        }
    ]

    request_data = {
        "locale": "tr",
        "conversationId": "123456789",
        "price": "10",
        "paidPrice": "10",
        "currency": "TRY",
        "basketId": "B67832",
        "paymentGroup": "PRODUCT",
        "callbackUrl": "http://localhost:8000/payment/callback/",
        "enabledInstallments": ["2", "3", "6", "9"],
        "buyer": {
            "id": "BY789",
            "name": "Adınız",
            "surname": "Soyadınız",
            "gsmNumber": "+905350000000",
            "email": "email@example.com",
            "identityNumber": "74300864791",
            "lastLoginDate": "2020-10-05 12:43:35",
            "registrationDate": "2013-04-21 15:12:09",
            "registrationAddress": "Adres Bilgisi",
            "ip": request.META.get("REMOTE_ADDR", "127.0.0.1"),
            "city": "Istanbul",
            "country": "Turkey",
            "zipCode": "34732"
        },
        "shippingAddress": {
            "contactName": "Ad Soyad",
            "city": "Istanbul",
            "country": "Turkey",
            "address": "Adres Bilgisi",
            "zipCode": "34742"
        },
        "billingAddress": {
            "contactName": "Ad Soyad",
            "city": "Istanbul",
            "country": "Turkey",
            "address": "Adres Bilgisi",
            "zipCode": "34742"
        },
        "basketItems": basket_items
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request_data, options)
    checkout_form_content = checkout_form_initialize.read().decode("utf-8")
    checkout_form = json.loads(checkout_form_content)

    return render(request, "store/payment.html", {
        "checkout_form_content": checkout_form["checkoutFormContent"]
    })


@login_required
def shipping_address_view(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save()
            return redirect('store:create_order', shipping_id=shipping_address.id)
    else:
        form = ShippingAddressForm()
    return render(request, 'store/shipping_address.html', {'form': form})

@login_required
def create_order(request, shipping_id):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:home')
    
    shipping = get_object_or_404(ShippingAddress, id=shipping_id)

    order = Order.objects.create(
        user=request.user,
        status='Paid',
        shipping_address=shipping
    )

    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        total += product.price * quantity

    #Toplam Fiyat Kaydet base.html kısmı
    order.total_price = total
    order.save()



    # Sepeti temizle
    request.session['cart'] = {}

    return redirect('store:order_summary', order_id=order.id)

    
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = []
    total = 0
    for item in order.items.all():
        subtotal = item.price * item.quantity
        total += subtotal
        items.append({
            'product': item.product,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': subtotal,
        })
    context = {
        'order': order,
        'items': items,
        'total': total,
    }
    return render(request, "store/order_summary.html", context)


# @csrf_exempt
# def payment_callback(request):
#     conversation_id = request.POST.get('conversationId')

#     if not conversation_id:
#         return HttpResponse("conversationId yok", status=400)
    
#     order = get_object_or_404(Order, conversation_id=conversation_id)

#     order.status = 'paid'
#     order.save()

#     return redirect('store:order_summary', order_id=order.id)

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})