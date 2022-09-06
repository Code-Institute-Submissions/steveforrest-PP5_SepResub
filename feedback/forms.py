from django import forms
from .models import Response

# class FeedBackForm(forms.ModelForm):
#     """
#     creates a form using the feedback model
#     """
#     class Meta:
#         model = Response
#         exclude = ('',)
        
#     def __init__(self, *args, **kwargs):
#         """
#         Add placeholders and classes, remove auto-generated
#         labels and set autofocus on first field
#         """
#         super().__init__(*args, **kwargs)
#         placeholders = {
#             'user': 'Name',
#             'email': 'Email Address',
#             'phone_number': 'Phone number',
#             'issue': 'What situation  best discribes your feed back',
#             'comment': 'Please discribe the issue',
#         }
        

# class FeedBackForm(forms.Form):
#     """
#     creates a form using the feedback model
#     """
#     name = forms.CharField(label='Your name', max_length=100)
#     email = forms.CharField(label='Your email address', max_length=100)
#     phone_number = forms.CharField(label='Your phone number', max_length=100)
#     issue = forms.CharField(label='What issue are you experiencing', max_length=100)
#     comment = forms.CharField(label='Please discribe your issue', max_length=400)
    
    
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
            'email': 'Email Address',
            'phone_number': 'Phone number',
            'issue': 'What situation  best discribes your feed back',
            'comment': 'Please discribe the issue',
        }