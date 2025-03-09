from django.contrib import admin
from django.urls import path ,include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', home_redirect),

]

