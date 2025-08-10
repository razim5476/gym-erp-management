from rest_framework.views import APIView
from user.models import User
from . import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import response, permissions, status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class RegisterUserView(APIView):
    """API for registering the user."""

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserSerializer

    def post(self, request):

        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return response.Response({'success': 'Registration Succesful'}, status=status.HTTP_201_CREATED)
        return response.Response({'error': 'Something happened.Try again.'})


class UserLoginView(APIView):
    """API for the user login."""

    serializer_class = serializers.UserLoginSerializer

    def post(self, request):

        serializer = serializers.UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return response.Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """API for the user.CRUD operations."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'userr_type']
    ordering_fields = ['created_at', 'joined_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            return queryset.filter(is_active=True)
        else:
            return queryset

    def create(self, serializer):
        serializer.created_by = self.request.user
        serializer.save()

