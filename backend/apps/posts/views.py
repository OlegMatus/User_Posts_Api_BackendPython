from django.http import Http404
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.posts.models import PostModel
from apps.posts.serializers import PostSerializer


class PostListApiView(ListAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination


class UserPostListApiView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PostModel.objects.filter(user=self.request.user)


class PostCreateApiView(CreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostPerformUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_object(self):
        try:
            return PostModel.objects.get(user=self.request.user.id, id=self.kwargs['pk'])
        except PostModel.DoesNotExist:
            raise Http404('Post does not exist')

