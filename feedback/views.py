from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import FeedBackForm
from profiles.forms import ProfileForm
from .models import Response
from profiles.models import UserProfile
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse


def feedback(request):
    """
    Display feedback template
    """
    if request.method == "GET":
        feedback_form = FeedBackForm()
        return render(request, 'feedback/feedback.html',
                      {"feedback_form": feedback_form})
    # sets up the initial sate of the form taken if the user has already
    # registered
    if request.method == 'POST':
        feedback_form = FeedBackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, 'feedback updated successfully')
            return redirect('/')
        else:
            messages.error(
                request, 'feedback not updated please check your form')
            return render(request, 'feedback/feedback.html',
                          {"feedback_form": feedback_form})
    template = 'feedback/feedback.html'
    return render(request, template)
