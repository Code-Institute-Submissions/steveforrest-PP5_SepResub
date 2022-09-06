from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import FeedBackForm
from profiles.forms import ProfileForm
from .models import Response
from profiles.models import UserProfile


def feedback(request):
    """
    Display feedback template
    """
    if request.method == "GET":
        feedback_form = FeedBackForm() 
        return render(request, 'feedback/feedback.html', {"feedback_form":feedback_form})
    # # sets up the initial sate of the form taken if the user has already
    # # registered
    # if request.method == 'POST':
    #     form = FeedBackForm(request.POST, instance=profile)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'feedback updated successfully')
    #     else:
    #         messages.error(
    #             request, 'feedback not updated please check your form')
    #         form = ProfileForm()

    # template = 'feedback/feedback.html'
    # context = {
    #     'user': user,
    #     'test': 'Work?/',

    # }
    

    return render(request, template, context)
