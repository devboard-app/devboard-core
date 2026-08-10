from typing import ClassVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsInternalService
from .serializers import UserProfileSerializer

# Create your views here.

class SyncUserView(APIView):
    permission_classes : ClassVar =  [IsInternalService]
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    