from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.user.managers import UserManager

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['email', 'password']

        objects = UserManager()

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
