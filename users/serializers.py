from typing import ClassVar

from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'email', 'name', 'avatar', 'timezone', 'role', 'status', 'last_active', 'created_at', 'updated_at']
        read_only_fields: ClassVar = ['user_id', 'email', 'role', 'status', 'last_active', 'created_at', 'updated_at']

class UserSyncSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[]) ##to ignore email duplicate check
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'email', 'role']

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['status']
