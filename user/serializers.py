"""
Serializer for the user app.
"""

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from core.serializers import ReadOnlyFieldsSerializer
from user.models import User
from django.contrib.auth import authenticate


class MinimalUserSeriaizer(serializers.ModelSerializer):
    """Minimal User.minimal fields."""

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname']


class UserSerializer(ReadOnlyFieldsSerializer, serializers.ModelSerializer):
    """Serializer for the user."""

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'password', 'password2', 'age', 'image', 'userr_type', 'is_trainer', 'height', 'weight', 'email', 'phone_number', 'created_at', 'updated_at', 'created_by', 'role']

    def validate(self, attrs):

        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError('Password do not match.')
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(password=validated_data['password'])
        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer for the user login."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):

        email = attrs.get['email']
        password = attrs.get['password']

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email not registered. Please sign up first.')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid username or password.')

        attrs['user'] = user
        return attrs
