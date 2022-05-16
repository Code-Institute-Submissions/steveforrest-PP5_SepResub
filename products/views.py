from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        return render(request, 'products/product_search_result.html', { 'products': products })
        if 'q' in request.GET:
            query = request.GET['q']
            if query:
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries)
            else:
                messages.error(request, "You didn't enter any search criteria!")       
            return render(request, 'products/product_search_result.html', { 'products': products })
    
    pizzas = products.filter(
        Q(category__name__contains='Pizza')
    )
    burgers = products.filter(
        Q(category__name__contains='burgers')
    )
    fries = products.filter(
        Q(category__name__contains='fries')
    )
    extras = products.filter(
        Q(category__name__contains='extras')
    )
    drinks = products.filter(
        Q(category__name__contains='drinks')|
        Q(category__name__contains='hot')|
        Q(category__name__contains='shakes')|
        Q(category__name__contains='pop')
    )
    worlds = products.filter(
        Q(category__name__contains='world_food')|
        Q(category__name__contains='greek')|
        Q(category__name__contains='curry')
    )
    desserts = products.filter(
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
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def identify_product(request, pk):
    """a View that searches to help with generating the products in the products html"""
    if request.method == 'GET':
        product = get_object_or_404(Product, id=pk)
        context = {
            'product': product
        }
        return render(request, 'products/snippets/product_card.html', context)
    else:
        return HttpResponse('error')
    