from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.authentication.views import RegisterView

urlpatterns = [
    path('/register', RegisterView.as_view(), name='auth_register'),
    path('/login', TokenObtainPairView.as_view(), name='auth_login'),
]
