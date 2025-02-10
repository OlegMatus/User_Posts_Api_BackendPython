from rest_framework import serializers

from apps.posts.models import PostModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id','user', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
        extra_kwargs = {}

        def validate_content(self, value):
            if not value.strip():
                raise serializers.ValidationError("Текст не може бути порожнім")
            return value

        def create(self, validated_data:dict):
           return PostModel.objects.create(**validated_data)