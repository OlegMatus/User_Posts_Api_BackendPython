from django.urls import path
from .views import PostListApiView, UserPostListApiView, PostCreateApiView, PostPerformUpdateDestroyApiView

urlpatterns = [
    path('', PostListApiView.as_view(), name='post-list'),
    path('/user/posts', UserPostListApiView.as_view(), name='user-post-list'),
    path('/create', PostCreateApiView.as_view(), name='post-create'),
    path('/post/<int:pk>', PostPerformUpdateDestroyApiView.as_view(), name='post-update'),
]