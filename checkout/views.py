from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    order = request.session.get('order', {})
    if not order:
        messages.error(request, "There's nothing in your basket!")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51KltltEMq4WemSuSjy4nCFK3zkAsOhRkO7JnPSFqN69JqwPjsWvElZYU8IZ7Mc847seLbaVPAVP4j62RlzTXcj2l00pfp6hpcH',
        'client_secret': 'test client secret',
    }
    
    return render(request, template, context)