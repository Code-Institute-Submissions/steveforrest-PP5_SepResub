from django.shortcuts import render, redirect

# Create your views here.

def view_order(request):
    """A view to return the home, index page"""
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """view for getting the quantity to add to the bag"""
    
    quantity = str(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        
    request.session['bag'] = bag
    return redirect(redirect_url)