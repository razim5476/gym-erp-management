"""
Docstring for authentication.serializers.serializers
"""


from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from core.utils import generate_unique_id
from organization.models import Branch, Company
from user.models import Address, Role



User = get_user_model()




class LoginSerializer(serializers.Serializer):
    """
    Login Serializer.
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        

        attrs['user'] = user
        return attrs

