from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category, Review
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator



# Create your views here.

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
                          {'products': products})
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
                    f"You didn't enter any search criteria, all {searchSize} were returned")
            return render(request, 'products/product_search_result.html',
                          {'products': products, 'searchSize': searchSize})

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
        Q(category__name__contains='drinks') |
        Q(category__name__contains='hot') |
        Q(category__name__contains='shakes') |
        Q(category__name__contains='pop')
    )
    worlds = products.filter(
        Q(category__name__contains='world_food') |
        Q(category__name__contains='greek') |
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
        'categories': categories,
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
                'Failed to add product. please ensure all fields are completed correctly')
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
    template_name = 'products/templates/products/review_form.html'
    model = Review

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Succesfully reviewed the product')
        return super(CreateView, self).form_valid(form)


# class ViewReviews(ListView):
#     """ A view to return a list of reviews """
#     def get(self, request):
#         # <view logic>
        
#         return render(request, 'detail_product', context)
    
def productDetail(request):
    """

    """
    return render(request, 'products/templates/products/product_review.html')



@csrf_protect
@login_required
def post_roster(request):

    """
    View to allow user to post a new review

    """

    # create an empty form  to post into the table
    form = ReviewForm()

    if request.method == 'POST':
        # handle the post and save the form data
        form = ReviewForm(request.POST)
        # if the form is valid
        if form.is_valid():

            new_form = form.save(commit=False)
            # check if user is authenticated if so use their
            # username if not use guest as created_by
            if request.user.is_authenticated:
                new_form.created_by = request.user
            else:
                return redirect(reverse('detail_product'))

            new_form.status = 1
            new_form.save()

        return redirect(reverse('detail_product'))

    else:
        form = RosterForm()

    return render(request, 'review_product.html', {
        'roster_form': form, 'comment_form': CommentForm()
        })
    
    
@method_decorator(login_required)
def post(self, request, id, *args, **kwargs):
    """
    function to allow view to post to db
    """
    post = Review.objects.get(pk=id)
    user = User.objects.get(username=request.user.username)
    # handle the post and save the form data
    form = CommentForm(request.POST)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.post = post
        new_form.commenter = user
        new_form.save()
        # add the user to the Comments field of the Review
        post.list_comments.add(user)
        # save the RosterList
        post.save()
    context = {
        'comments': comments,
    }
    # use the post variable which gets the object needed to
    # be acounted by it's id and create a variable set it to
    # count and call the method created to count the likes in the model

    context['review_form'] = ReviewForm()

    return HttpResponseRedirect(reverse('roster-detail', args=[id]))