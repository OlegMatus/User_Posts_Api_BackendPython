import uuid

from django.utils.timezone import now
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from apps.user.models import UserSessionModel
from apps.user.serializers import UserSerializer
from core.services.jwt_service import JWTService

from core.services.jwt_service import ActivateToken

UserModel = get_user_model()


class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def patch(*args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class LoginUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        email = request.data['email']
        password = request.data['password']

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(UserModel, email=email)

        if not user.is_active:
            return Response({'error': 'User account is disabled'}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        UserSessionModel.objects.create(
            user=user,
            session_id=str(uuid.uuid4())
        )

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data['refresh']
            print(refresh_token)

            token = RefreshToken(refresh_token)

            try:
                token.blacklist()
            except InvalidToken:
                pass

            last_session = UserSessionModel.objects.filter(user=request.user, ended_at__isnull=True, ).order_by(
                '-created_at').first()
            if last_session:
                last_session.ended_at = now()
                last_session.save()

            return Response({'message': 'Logged out successfully'}, status.HTTP_200_OK)

        except InvalidToken:
            return Response({'error': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({'error': 'Unexpected error occurred'}, status=status.HTTP_400_BAD_REQUEST)
