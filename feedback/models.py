from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from profiles.models import UserProfile

# Create your models here.

ISSUE = (
        (1,'Delivery time'),
        (2,'Customer service'),
        (3,'Food quality'),
        (4,'Something else'),
)

class Response(models.Model):
        """
        Modal for the feedback form
        """
        user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
        guest = models.CharField(max_length=50, null=False, blank=False)
        email = models.EmailField(max_length=254, null=False, blank=False)
        phone_number = models.CharField(max_length=20, null=False, blank=False)
        issue = models.IntegerField(choices=ISSUE)
        comment = RichTextField(max_length=10000, null=False, blank=False)
