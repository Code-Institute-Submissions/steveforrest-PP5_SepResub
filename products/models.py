from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    # link to a primary key in categories model
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


RATING = (
    (0, '0'),
    (0.5, '0.5'),
    (1, '1'),
    (1.5, '1.5'),
    (2, '2'),
    (2.5, '2.5'),
    (3, '3'),
    (3.5, '3.5'),
    (4, '4'),
    (4.5, '4.5'),
    (5, '5'),
    (5.5, '5.5'),
    (6, '6'),
    (6.5, '6.5'),
    (7, '7'),
    (7.5, '7.5'),
    (8, '8'),
    (8.5, '8.5'),
    (9, '9'),
    (9.5, '9.5'),
    (10, '10'),
    )


class Review(models.Model):
    """
    Adds review to product
    """
    review = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = RichTextField(max_length=10000, null=False, blank=False)
    # review is a new entry so the name of the person adding the comment
    # can be recorded
    raviewer = models.ForeignKey(User, on_delete=models.CASCADE,
                                 null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(choices=RATING)

    class Meta:
        ordering = ['-created_on']


ALLERGEN = (
    (1, 'Gluten'),
    (2, 'Lactose'),
    (3, "Eggs"),
    (4, "Peanuts"),
    (5, "Fish"),
    (6, "Shellfish"),
    (7, "Kosha"),
    (8, "Halal"),
)


class DietRequirements(models.Model):
    """
    Model for adding allegens to the products
    """
    assignedProduct = models.ForeignKey(Product, on_delete=models.CASCADE,
                                        null=True, blank=True, related_name='requirements')
    allergens = models.IntegerField(choices=ALLERGEN)
    
