from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from backend.apps.auth.views import RegisterView, ActivateUserView
from backend.apps.auth.views import LoginUserView, LogoutUserView

urlpatterns = [
    path('/register', RegisterView.as_view(), name='auth_register'),
    path('/login', LoginUserView.as_view(), name='auth_login'),
    path('/logout', LogoutUserView.as_view(), name='auth_logout'),
    path('/refresh', TokenRefreshView.as_view(), name='auth_refresh'),
    path('/activate/<str:token>', ActivateUserView.as_view(), name='auth_activate')

]
