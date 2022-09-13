from django.contrib import admin
from .models import Product, Category, Review, DietRequirements
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'image',
    )
    orderinng = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'comment',
        'raviewer',
        'rating',
    )

    
class DietRequirementsAdmin(admin.ModelAdmin):
    """
    adds ability to access model in admin page
    """
    list_display = (
        'assignedProduct',
        'allergens',
        'id',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(DietRequirements, DietRequirementsAdmin)

