"""
Docstring for authentication.serializers.serializers
"""


from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers



User = get_user_model()




class LoginSerializer(serializers.Serializer):
    """
    Login Serializer.
    """

    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username') or attrs.get('email')
        password = attrs.get('password')

        if not username:
            raise serializers.ValidationError("Username or email is required.")

        user_obj = User.objects.filter(email=username).first()
        username = user_obj.username if user_obj else username
        request = self.context.get('request')
        user = authenticate(request=request, username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        

        attrs['user'] = user
        return attrs

