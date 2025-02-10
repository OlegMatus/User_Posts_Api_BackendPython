from django.urls import path
from .views import UserListCreateView, UserSearchByView, UserDestroyUpdateApiView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list'),
    path('/search', UserSearchByView.as_view(), name='user_search'),
    path('/me', UserDestroyUpdateApiView.as_view(), name='user_me'),
]
