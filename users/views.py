from typing import ClassVar

from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import AsyncAPIView

from .permissions import IsInternalService
from .repository import get_user_by_id
from .serializers import UserProfileSerializer, UserSyncSerializer


class SyncUserView(AsyncAPIView):
    permission_classes : ClassVar =  [IsInternalService]
    async def post(self, request):
        print(request.data)
        instance = await get_user_by_id(request.data.get('user_id'))
        serializer = UserSyncSerializer(instance, data=request.data)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(AsyncAPIView):
    permission_classes: ClassVar = [IsAuthenticated]
    async def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    async def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
