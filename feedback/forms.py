from django import forms
from .models import Response


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'user': 'Name',
            'guest': 'Name',
            'email': 'Email Address',
            'phone_number': 'Phone number',
            'issue': 'What situation  best discribes your feed back',
            'comment': 'Please discribe the issue',
        }
