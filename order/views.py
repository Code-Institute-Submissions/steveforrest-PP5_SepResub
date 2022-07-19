from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


# Create your views here.

def view_order(request):
    """
    Function to view the order page

    input parameters
    request: object coming from the client

    return parameter
    render to the order/order.html url
    """
    return render(request, 'order/order.html')


def add_to_order(request, item_id):
    """
    Function to add items to order

    input parameters
    request: object coming from the client
    item_id: id of the object to be added to the order

    return parameter
    redirection to new URL
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('qty'))
    redirect_url = request.POST.get('redirect_url')
    order = request.session.get('order', {})

    if item_id in list(order.keys()):
        order[item_id] += quantity
        messages.success(
            request,
            f'Added {product.name} to your {order[item_id]}')
    else:
        order[item_id] = quantity
        messages.success(request, f'Added {product.name} to your order')

    request.session['order'] = order
    return redirect(redirect_url)


def adjust_order(request, item_id):
    """
    Function to adjust the items in the order

    input parameters
    request: object coming from the client
    item_id: id of the object to be added to the order

    return parameter
    redirection revers to view_order
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    order = request.session.get('order', {})

    if quantity > 20:
        messages.info(request, f'Quantity too high must be below 21')
        redirect_url = request.POST.get('redirect_url')
    elif quantity < 1:
        messages.info(request, f'Quantity too low must be higher than 0')
        redirect_url = request.POST.get('redirect_url')
    else:
        if item_id in list(order.keys()):
            order[item_id] = quantity
            messages.info(
                request,
                f'adjusted {product.name} on your order to {order[item_id]} portions')
        else:
            order.pop(item_id)
            messages.info(
                request,
                f'adjusted {product.name} on your order to {order[item_id]} portions')

    request.session['order'] = order
    return redirect(reverse('view_order'))


def remove_from_order(request, item_id):
    """
    Function to remove items from the order

    input parameters
    request: object coming from the client
    item_id: id of the object to be added to the order

    return parameter
    HttpRespone = 200
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        order = request.session.get('order', {})

        order.pop(item_id)
        messages.info(request, f'removed {product.name} from your order')

        request.session['order'] = order
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item {e}')
        return HttpResponse(status=500)
