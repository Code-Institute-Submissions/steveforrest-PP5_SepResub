from django.shortcuts import render

def profile(request):
    """
    Display profile template
    """
    template = 'profiles/profile.html'
    context = {
        
    }
    
    return render(request, template, context)

