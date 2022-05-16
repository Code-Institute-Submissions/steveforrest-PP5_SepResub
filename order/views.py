from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from products.models import Product



# Create your views here.

def view_order(request):
    """A view to return the home, index page"""
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """view for getting the quantity to add to the order"""
    
    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('qty'))
    redirect_url = request.POST.get('redirect_url')
    order = request.session.get('order', {})
    
    if item_id in list(order.keys()):
        order[item_id] += quantity
        messages.success(request, f'Added {product.name} to your {order[item_id]}')
    else:
        order[item_id] = quantity
        messages.success(request, f'Added {product.name} to your order')
        
    request.session['order'] = order
    return redirect(redirect_url)


def adjust_order(request, item_id):
    """view for adjusting the order"""
    
    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    order = request.session.get('order', {})
    
    if item_id in list(order.keys()):
        order[item_id] = quantity
        messages.info(request, f'adjusted {product.name} on your {order[item_id]}')
    else:
        order.pop(item_id)
        messages.info(request, f'removed {product.name} from your order')
        
    request.session['order'] = order
    return redirect(reverse('view_order'))


def remove_from_order(request, item_id):
    """view for adjusting the order"""
    
    try:
        product = Product.objects.get(pk=item_id)
        order = request.session.get('order', {})
        
        if item_id in list(order.keys()):
            order[item_id] = quantity
            messages.info(request, f'adjusted {product.name} on your {order[item_id]}')
        else:
            order.pop(item_id)
            messages.info(request, f'removed {product.name} from your order')
            
        request.session['order'] = order
        return HttpResponse(status=200)
    except exception as e:
        return HTTpResponse(status=500)