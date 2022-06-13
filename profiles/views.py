from django.shortcuts import render, get_object_or_404
from django.contrib import messages


from .forms import ProfileForm
from .models import UserProfile

from checkout.models import Invoice

def profile(request):
    """
    Display profile template
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    # sets up the initial sate of the form taken if the user has already registered
    profile_form = ProfileForm(initial={
        'full_name': profile.user.get_full_name(),
        'email': profile.user.email,
        'phone_number': profile.default_phone_number,
        'country': profile.default_country,
        'postcode': profile.default_postcode,
        'town_or_city': profile.default_town_or_city,
        'street_address1': profile.default_street_address1,
        'street_address2': profile.default_street_address2,           
        'county': profile.default_county,
        })
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully')
        else:
            messages.error(request,'Profile not updated please check your form')
            form = ProfileForm()
        
    # profile_form = ProfileForm
    orders = profile.orders.all()
    
    template = 'profiles/profile.html'
    context = {
        'orders': orders,
        'profile_form': profile_form,
        'on_profile_page': True,
    }
    
    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Invoice, order_number=order_number)
    messages.info(request, (
         f'This is a past confirmation for order number { order_number }.'
         'A confirmation email was sent on the order date. '
     ))
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }
    
    return render(request, template, context)