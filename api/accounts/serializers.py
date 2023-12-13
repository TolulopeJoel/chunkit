from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .validators import UserValidator


class UserSerializer(UserValidator, serializers.ModelSerializer):
    """
    Serializer for the user model.
    """
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'first_name',
            'password',
            'password2'
        ]

    def create(self, validated_data):
        """
        Create a new user using the validated data.
        """
        validated_data.pop('password2')
        validated_data['username'] = validated_data['email']
        return get_user_model().objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
