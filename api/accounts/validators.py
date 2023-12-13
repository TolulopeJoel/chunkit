from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserValidator:
    def validate_email(self, email):
        """
        Validate email to ensure it's unique.
        """
        user_q = get_user_model().objects.filter(username=email).first()
        if user_q:
            raise serializers.ValidationError(
                'A user with this email already exists'
            )

        return email

    def validate(self, attrs):
        """
        Validate the password and password2 fields to ensure they match.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')

        return attrs
