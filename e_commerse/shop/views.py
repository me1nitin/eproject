from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product
from django.core.paginator import Paginator, InvalidPage, EmptyPage


# Create your views here.
def allprodcat(request, c_slug=None):
    c_page = None
    products = None
    cat = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        product_list = Product.objects.all().filter(category=c_page, avail=True)
    else:
        product_list = Product.objects.all().filter(avail=True)
        cat = Category.objects.all()
    paginator = Paginator(product_list, 6)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except(InvalidPage, EmptyPage):
        products = paginator.page(paginator.num_page)

    return render(request, 'category.html', {'category': c_page, 'products': products, 'cat': cat})


def productdetail(request, c_slug, p_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=p_slug)
    except Exception as e:
        raise e
    return render(request, 'prod_detail.html', {'product': product})
