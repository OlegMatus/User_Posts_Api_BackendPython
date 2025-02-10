from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers

from apps.user.models import ProfileModel

from core.services.email_service import EmailService

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = (
            'id',
            'first_name',
            'last_name',
            'age',
            'created_at',
            'updated_at',
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'profile'
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        EmailService.register(user)

        return user

    def update(self, instance, validated_data: dict):
        profile_data = validated_data.pop('profile')

        if profile_data:
            profile = instance.profile or ProfileModel(user=instance)
            profile.first_name = profile_data.get('first_name', profile.first_name)
            profile.last_name = profile_data.get('last_name', profile.last_name)
            profile.age = profile_data.get('age', profile.age)
            profile.save()

        if not instance.profile:
            instance.profile = profile

        instance.save()
        return instance
