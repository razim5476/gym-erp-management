from rest_framework.views import APIView
from rest_framework import viewsets, generics, mixins
from rest_framework import permissions, status, response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from . import serializers
from django.db import transaction

# Create your views here.


class BranchSettingsView(APIView):
    """View set fo rthe branch model. for create branch with settings"""

    serializer_class = serializers.BranchSettingsSerializer

    def post(self, request):

        user = self.request.user
        serializer = serializers.CombinedBranchWithSettingsSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()

                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
