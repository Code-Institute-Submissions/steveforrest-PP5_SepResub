from django import forms
from.models import Product, Category

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.obejects.all()
        friendly_name = [(c.id, c.get_friendly_name()) for c in categories]
        
        self.field['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'