from django.urls import path, include

urlpatterns = [
    path('api/users', include('apps.user.urls')),
    path('api/auth', include('apps.auth.urls')),
    path('api/posts', include('apps.posts.urls')),
]
