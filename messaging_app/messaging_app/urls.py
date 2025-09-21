from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),         # Your app routes
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
]
