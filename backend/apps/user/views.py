from functools import partial

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from apps.user.filter import UserFilter
from apps.user.models import ProfileModel
from apps.user.serializers import UserSerializer
from apps.user.services import UserService

UserModel = get_user_model()


class UserListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [AllowAny]


class UserDestroyView(DestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer()
    permission_classes = [IsAuthenticated]


class UserSearchByView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user_id = self.request.query_params.get('id')
        email = self.request.query_params.get('email')

        if not user_id and not email:
            raise ValidationError({'error': 'You must provide id or email parameter.'},
                                  status.HTTP_400_BAD_REQUEST)

        user_service = UserService()

        if user_id:
            user = user_service.search_by_id(user_id)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif email:
            user = user_service.search_by_email(email)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserDestroyUpdateApiView(RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_object(self, *args, **kwargs):
        user = self.request.user

        user.profile, created = ProfileModel.objects.get_or_create(user=user)
        return user

    def patch(self, *args, **kwargs):
        user = self.get_object()

        profile_data = self.request.data.get('profile')
        if profile_data:
            ProfileModel.objects.filter(user=user).update(**profile_data)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
