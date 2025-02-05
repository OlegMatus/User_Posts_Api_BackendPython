from django.urls import path, include

urlpatterns = [
    path('api/users', include('apps.user.urls')),
    path('api/auth', include('apps.authentication.urls'))
]
