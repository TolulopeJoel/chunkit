from rest_framework import serializers


class UserValidator:
    def validate(self, attrs):
        """
        Validate the password and password2 fields to ensure they match.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')

        return attrs
