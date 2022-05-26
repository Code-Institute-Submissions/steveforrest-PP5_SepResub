from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def order_contents(request):
    
    order_items = []
    total = 0
    sub_total = 0
    product_count = 0
    order = request.session.get('order', {})
    FREE_DELIVERY_THRESHOLD = settings.FREE_DELIVERY_THRESHOLD
    free_delivery_shortfall = 0
    
    for item_id, item_data in order.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            order_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'total':total,
            })
    
    if (total < settings.FREE_DELIVERY_THRESHOLD) & (product_count > 0):
        free_delivery_shortfall = settings.FREE_DELIVERY_THRESHOLD - total
        grand_total = settings.DELIVERY_CHARGE + total
    else:
        grand_total =  total
    
    context = {
        'order_items': order_items,
        'total': total,
        'product_count': product_count,
        'FREE_DELIVERY_THRESHOLD': FREE_DELIVERY_THRESHOLD,
        'free_delivery_shortfall': free_delivery_shortfall,
        'grand_total': grand_total,
    }
    return context