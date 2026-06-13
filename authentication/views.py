from rest_framework_simplejwt.tokens import RefreshToken
from .serializers.serializers import LoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.



class LoginAPIView(APIView):
    """
    Login APIView
    """

    def post(self, request):


        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user=user)

            return Response({
                "success": True,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.get_full_name(),
                }
            })
    

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
