from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from core.responses import error_response, success_response
from user.models import LoginLog
from user.serializers.serializers import make_model_id
from .serializers.serializers import LoginSerializer



class LoginAPIView(APIView):
    """
    Login APIView
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user=user)

            LoginLog.objects.create(
                login_log_id=make_model_id("LoginLog", "LOGIN", request),
                user=user,
                description="User logged in successfully.",
                created_by=user,
            )

            return success_response(
                message="Logged in successfully.",
                data={
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "user_id": user.user_id,
                    "email": user.email,
                    "name": " ".join(
                        part for part in [user.first_name, user.last_name] if part
                    ),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "is_superuser": user.is_superuser,
                    "is_staff": user.is_staff,
                    "company": {
                        "id": user.company.id,
                        "name": user.company.name,
                    } if user.company else None,
                    "branch": {
                        "id": user.branch.id,
                        "name": user.branch.name,
                    } if user.branch else None,
                    "image": user.image.url if user.image else None,
                    "roles": list(user.role.values("id", "role_id", "name")),
                }
                },
            )

        return error_response(
            message="Validation failed.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class LogoutAPIView(APIView):
    """
    Logout APIView.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return error_response(
                message="Refresh token is required.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return error_response(
                message="Invalid or expired refresh token.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(message="Logged out successfully.")


