from typing import ClassVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsInternalService
from .repository import get_user_by_id
from .serializers import UserSyncSerializer

# Create your views here.

class SyncUserView(APIView):
    permission_classes : ClassVar =  [IsInternalService]
    def post(self, request):
        instance = get_user_by_id(request.data.get('user_id'))
        serializer = UserSyncSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    