from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    update order total onlineitem update/create
    """
    instance.invoice.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_deletse(sender, instance, **kwargs):
    """
    update order total onlineitem delete
    """
    instance.invoice.update_total()
