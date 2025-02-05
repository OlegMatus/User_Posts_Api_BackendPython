from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
# from core.services.jwt_service import JWTService

from apps.authentication.serializers import RegisterSerializer

UserModel = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user=user)
        access = str(refresh.access_token)

        return Response({
            "user": serializer.data,
            "access": access,
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)

class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        JWTService
