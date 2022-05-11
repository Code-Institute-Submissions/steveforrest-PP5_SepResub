from django.shortcuts import render, redirect

# Create your views here.

def view_order(request):
    """A view to return the home, index page"""
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """view for getting the quantity to add to the order"""
    
    quantity = int(request.POST.get('qty'))
    redirect_url = request.POST.get('redirect_url')
    order = request.session.get('order', {})
    
    if item_id in list(order.keys()):
        order[item_id] += quantity
    else:
        order[item_id] = quantity
        
    request.session['order'] = order
    return redirect(redirect_url)