from django.conf import settings

def order_contents(request):
    
    order_items = []
    total = 0
    product_count = 0
    FREE_DELIVERY_THRESHOLD = settings.FREE_DELIVERY_THRESHOLD
    
    
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = 5
        free_delivery_shortfall = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery= 0
        free_delivery_shortfall = 0
    
    grand_total = delivery + total
    
    context = {
        'order_items': order_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'FREE_DELIVERY_THRESHOLD': FREE_DELIVERY_THRESHOLD,
        'free_delivery_shortfall': free_delivery_shortfall,
        'grand_total': grand_total,
    }
    return context