from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model.
    """
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
        return get_user_model().objects.create_user(**validated_data)

    def validate(self, attrs):
        """
        Validate the password and password2 fields to ensure they match.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
