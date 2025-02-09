from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

UserModel = get_user_model()


class UserService:
    @staticmethod
    def search_by_id(user_id):
        return get_object_or_404(UserModel, pk=user_id)

    @staticmethod
    def search_by_email(email):
        return get_object_or_404(UserModel, email=email)
