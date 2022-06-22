from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import ProductForm
from django.contrib.auth.decorators import login_required



# Create your views here.

def all_products(request):
    """ 
    A view to show all products, including sorting and search queries 
    """

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


def identify_product(request, id):
    """
    a View that searches to help with generating the products in the products html
    """
    if request.method == 'GET':
        product = get_object_or_404(Product, id=id)
        context = {
            'product': product
        }
        return render(request, 'products/snippets/product_card.html', context)
    else:
        return HttpResponse('error')
    
    
@login_required    
def add_product(request):
    """
    Add products to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store admins can access this part of the site')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully added new product!')
            return redirect(reverse('products'))
        else:
            messages.error(request, 'Failed to add product. please ensure all fields are completed correctly')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)


@login_required
def edit_product(request, id):
    """
    Edit products to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store admins can access this part of the site')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully edited product!')
            return redirect(reverse('products'))
        else:
            messages.error(request, 'Failed to edit product!')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are now editing { product.name }')
    
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, template, context)


@login_required
def delete_product(request, id):
    """deletes a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store admins can access this part of the site')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect(reverse('products'))