from typing import ClassVar

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import validated
from core.views import AsyncAPIView

from .permissions import IsAdmin, IsInternalService
from .repository import (
    get_all_users,
    get_user_by_id,
    get_users_by_usernames,
)
from .serializers import (
    UserLookupInputSerializer,
    UserLookupSerializer,
    UserProfileInputSerializer,
    UserProfileSerializer,
    UserRoleInputSerializer,
    UserStatusInputSerializer,
    UserSyncInputSerializer,
)
from .services import (
    get_user_by_email_or_404,
    get_user_or_404,
    sync_user,
    update_profile,
    update_user_role,
    update_user_status,
)


class SyncUserView(AsyncAPIView):
    permission_classes : ClassVar = [IsInternalService]

    async def post(self, request):
        data = validated(UserSyncInputSerializer, request.data)
        instance = await get_user_by_id(str(data['user_id']))
        user, created = await sync_user(instance, data)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, response_status)

class MeView(AsyncAPIView):
    permission_classes: ClassVar = [IsAuthenticated]

    async def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    async def patch(self, request):
        data = validated(UserProfileInputSerializer, request.data)
        user = await update_profile(request.user, data)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserStatusView(AsyncAPIView):
    permission_classes: ClassVar = [IsAuthenticated, IsAdmin]

    async def patch(self, request, user_id):
        user = await get_user_or_404(user_id)
        data = validated(UserStatusInputSerializer, request.data)
        user = await update_user_status(user, data['status'])
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRoleView(AsyncAPIView):
    permission_classes: ClassVar = [IsAuthenticated, IsAdmin]

    async def patch(self, request, user_id):
        user = await get_user_or_404(user_id)
        data = validated(UserRoleInputSerializer, request.data)
        user = await update_user_role(user, data['role'])
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserByEmailView(AsyncAPIView):
    permission_classes: ClassVar = [IsInternalService]

    async def get(self, request):
        email = request.query_params.get('email')
        if not email:
            raise ValidationError({'email': 'Email query parameter is required.'})
        user = await get_user_by_email_or_404(email)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserListView(AsyncAPIView):
    permission_classes: ClassVar =[IsAuthenticated, IsAdmin]

    async def get(self, request):
        users = await get_all_users()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(AsyncAPIView):
    permission_classes: ClassVar =[IsAuthenticated]

    async def get(self, request, user_id):
        user = await get_user_or_404(user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class UserLookupView(AsyncAPIView):
    permission_classes: ClassVar = [IsInternalService]

    MAX_USERNAMES = 25

    async def post(self, request):
        data= validated(UserLookupInputSerializer, request.data)
        usernames = list({u.lower() for u in data['usernames'] if u})[:self.MAX_USERNAMES]
        if not usernames:
            return Response([], status=status.HTTP_200_OK)

        users = await get_users_by_usernames(usernames)
        serializer = UserLookupSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)