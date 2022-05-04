from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.http import HttpResponse


# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    pizzas = Product.objects.filter(
        Q(category__name__contains='Pizza')
    )
    burgers = Product.objects.filter(
        Q(category__name__contains='burgers')
    )
    fries = Product.objects.filter(
        Q(category__name__contains='fries')
    )
    extras = Product.objects.filter(
        Q(category__name__contains='extras')
    )
    drinks = Product.objects.filter(
        Q(category__name__contains='drinks')
    )
    worlds = Product.objects.filter(
        Q(category__name__contains='world_food')
    )
    desserts = Product.objects.filter(
        Q(category__name__contains='dessert')
    )
    context = {
        'products': products,
        'pizzas': pizzas,
        'burgers': burgers,
        'fries': fries,
        'extras': extras,
        'drinks': drinks,
        'worlds': worlds,
        'desserts': desserts,
    }

    return render(request, 'products/products.html', context)


def identify_product(request, pk):
    """a View that searches to help with generating the products in the products html"""
    if request.method == 'GET':
        product = get_object_or_404(Product, id=pk)
        context = {
            'product': product
        }
        # return HttpResponse('products/snippets/product_card.html')
        return render(request, 'products/snippets/product_card.html', context )
    
    else:
        return HttpResponse('error')