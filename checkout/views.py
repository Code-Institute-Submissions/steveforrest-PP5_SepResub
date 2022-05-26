from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Invoice
from products.models import Product
from order.context import order_contents

import stripe

def checkout(request):
    
    """
    view to pass the order amount over to stripe to make payment
    
    
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method =='POST':
        order = request.session.get('order', {})
        
        form_data = {
            'full_name':request.POST['full_name'],
            'email':request.POST['email'],
            'phone_number':request.POST['phone_number'],
            'country':request.POST['country'],
            'postcode':request.POST['postcode'],
            'town_or_city':request.POST['town_or_city'],
            'street_address1':request.POST['street_address1'],
            'street_address2':request.POST['street_address2'],
            'county':request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            invoice = order_form.save()
            for item_id, item_data in order.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        invoice=invoice,
                        product=product,
                        quantity=item_data,
                        )
                    order_line_item.save()
                except Product.DoesNotExist:
                    """
                    if item does not exit order will be deleted and 
                    returned to the shopping page
                    """
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    invoice.delete()
                    return redirect(reverse('view_order'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[invoice.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
                
    else:
        invoice = request.session.get('order', {})
        if not invoice:
            messages.error(request, "There's nothing in your basket!")
            return redirect(reverse('view_order'))
        
        # from order contexts
        current_order = order_contents(request)
        total = current_order['grand_total']
        stripe_total = round(total*100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        
        order_form = OrderForm()
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your enviroment?'
                         )
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    
    return render(request, template, context)


def checkout_success(request, order_number):
    """
    view to render a message when order successfully placed

    input parameters
    request: object coming from the client
    order_number: order number recieved from the request attached to the order

    return parameter
    renders to checkout/checkout_success.html
    using the context order
    """
    save_info = request.session.get('save')
    invoice = get_object_or_404(Invoice, order_number=order_number)
    messages.success(request, f'Order succesfully processed\
        Your order number is {order_number}. A confirmation \
        eail will be sent to {invoice.email}')
    
    if 'order' in request.session:
        del request.session['order']
    
    template = 'checkout/checkout_success.html'
    context = {
        'invoice' : invoice,
    }

    return render(request, template, context)