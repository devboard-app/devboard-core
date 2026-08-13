from typing import ClassVar

from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import AsyncAPIView

from .infrastructure import sync_user_role_to_auth, sync_user_status_to_auth
from .permissions import IsAdmin, IsInternalService
from .repository import get_all_users, get_user_by_id
from .serializers import (
    UserProfileSerializer,
    UserRoleSerializer,
    UserStatusSerializer,
    UserSyncSerializer,
)


class SyncUserView(AsyncAPIView):
    permission_classes : ClassVar =  [IsInternalService]
    async def post(self, request):
        instance = await get_user_by_id(request.data.get('user_id'))
        serializer = UserSyncSerializer(instance, data=request.data)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            response_status = status.HTTP_201_CREATED if instance is None else status.HTTP_200_OK
            return Response(serializer.data, response_status)
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserStatusView(AsyncAPIView):
    permission_classes: ClassVar = [IsAuthenticated, IsAdmin]

    async def patch(self, request, user_id):
        instance = await get_user_by_id(user_id)
        if instance is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserStatusSerializer(instance, data=request.data, partial=True)
        if await sync_to_async(serializer.is_valid)():
            await sync_user_status_to_auth(str(user_id), request.data['status'])
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRoleView(AsyncAPIView):
    permission_classes: ClassVar = [IsAuthenticated, IsAdmin]

    async def patch(self, request, user_id):
        instance = await get_user_by_id(user_id)
        if instance is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRoleSerializer(instance, data=request.data, partial=True)
        if await sync_to_async(serializer.is_valid)():
            await sync_user_role_to_auth(str(user_id), request.data['role'])
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(AsyncAPIView):
    permission_classes: ClassVar =[IsAuthenticated, IsAdmin]

    async def get(self, request):
        users = await get_all_users()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(AsyncAPIView):
    permission_classes: ClassVar =[IsAuthenticated]

    async def get(self, request, user_id):
        user = await get_user_by_id(user_id)
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        