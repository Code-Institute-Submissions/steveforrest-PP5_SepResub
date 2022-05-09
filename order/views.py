from django.shortcuts import render

# Create your views here.

def view_order(request):
    """A view to return the home, index page"""
    return render(request, 'order/order.html')