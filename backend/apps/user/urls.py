from django.urls import path
from .views import UserListCreateApiView, UserSearchByApiView, UserDestroyUpdateApiView

urlpatterns = [
    path('', UserListCreateApiView.as_view(), name='user_list'),
    path('/search', UserSearchByApiView.as_view(), name='user_search'),
    path('/me', UserDestroyUpdateApiView.as_view(), name='user_me'),
]
