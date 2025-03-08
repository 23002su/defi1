from django.shortcuts import render

def home(request):
    """
    Renders the main layout page (base.html).
    """
    return render(request, 'mainLayout.html')