from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from .widgets import CustomClearableFileInput
from djrichtextfield.widgets import RichTextWidget
from.models import Product, Category, Review


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput)

    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.obejects.all()
        friendly_name = [(c.id, c.get_friendly_name()) for c in categories]

        self.field['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'

        fields = ['comment', 'rating']

        labels = {
            'comment': 'comment',
            'rating': 'rating',
        }
        comment = forms.CharField()
