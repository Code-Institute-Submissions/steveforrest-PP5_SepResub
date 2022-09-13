from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category, Review, DietRequirements
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """

    products = Product.objects.all()
    query = None
    categories = []

    for c in products:
        categories.append(c.category)
        categories = list(dict.fromkeys(categories))

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            return render(request, 'products/product_search_result.html',
                            {'products': products,
                            })
        elif 'q' in request.GET:
            query = request.GET['q']
            if query:
                queries = (
                    Q(name__icontains=query) |
                    Q(category__name__icontains=query))
                products = products.filter(queries)
                searchSize = len(products)
            else:
                searchSize = len(products)
                messages.error(
                    request,
                    f"You didn't enter any search criteria,"
                    " all {searchSize} were returned")
            return render(request, 'products/product_search_result.html',
                          {'products': products, 'searchSize': searchSize})
    product = products.filter(
        Q(category__name__contains='query')
    )
    context = {
        'products': products,
        'product': product,
        'search_term': query,
        'categories': categories,
    }
    return render(request, 'products/products.html', context)


def identify_product(request, id):
    """
    a View that searches to help with generating
    the products in the products html
    """
    if request.method == 'GET':
        product = get_object_or_404(Product, id=id)
        context = {
            'product': product,
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
        messages.error(
            request,
            'Sorry only store admins can access this part of the site')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully added new product!')
            return redirect(reverse('products'))
        else:
            messages.error(
                request,
                'Failed to add product. please ensure all'
                ' fields are completed correctly')
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
        messages.error(
            request,
            'Sorry only store admins can access this part of the site')
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
        messages.error(
            request,
            'Sorry only store admins can access this part of the site')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect(reverse('products'))


class CreateReview(LoginRequiredMixin, CreateView):
    """
    A view to create a Review
    """
    form_class = ReviewForm
    template_name = 'products/product_review.html'
    model = Review

    def form_valid(self, form):
        """
        Posts a form underneath the reviews so new reviews can be posted
        """
        product = get_object_or_404(Product, id=self.kwargs['id'])
        form.instance.review = product
        form.instance.reviewer = self.request.user
        messages.success(self.request, 'Succesfully reviewed the product')
        # This is used as the success url rather than the absolute url
        self.success_url = f'/products/detail/{product.id}/'
        return super(CreateView, self).form_valid(form)


def product_detail(request, id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(review=id)
    context = {
        'product': product,
        'reviews': reviews,
        'form': ReviewForm(),
    }

    return render(request, 'products/product_review.html', context)
