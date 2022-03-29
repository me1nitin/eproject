from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# Creating card-id with session
def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(Cart_Id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(Cart_Id=cart_id(request))
    cart.save()

    try:
        cart_items = CartItem.objects.get(product=product, cart=cart)
        if cart_items.quantity < cart_items.product.stock:
            cart_items.quantity += 1
            cart_items.save()
    except CartItem.DoesNotExist:
        cart_items = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_items.save()
    return redirect('cart:cart_details')


def cart_details(request, tottal=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(Cart_Id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            tottal += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, tottal=tottal, counter=counter))


def cart_remove(request, product_id):
    cart = Cart.objects.get(Cart_Id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_details')


def full_remove(request, product_id):
    cart = Cart.objects.get(Cart_Id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_details')
