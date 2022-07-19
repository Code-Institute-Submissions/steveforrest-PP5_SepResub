from django.shortcuts import render


def index(request):
    """
    Function to view the order page

    input parameters
    request: object coming from the client

    return parameter
    render to the home/index.html url
    """
    return render(request, 'home/index.html')
