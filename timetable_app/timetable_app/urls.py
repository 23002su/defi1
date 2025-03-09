from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface
    path('scheduler/', include('scheduler.urls')),
    path('', include('users.urls')), # Include scheduler app URLs
]