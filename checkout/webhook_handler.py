from django.http import HttpResponse

class StripeWH_Handler:
    """
    Handle stripes webhooks
     
    """
    
    def __init__(self,request):
        """
        The init method of the class is a setup method that's called every time an instance of the class is created
        """
        self.request = request
        
    def handle_event(self,event):
        """
        Handle generic unknown/unexpected webhook event
        """
        