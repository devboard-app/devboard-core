from typing import ClassVar

from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'email', 'username', 'avatar', 'timezone', 'role', 'status', 'last_active', 'created_at', 'updated_at']
        read_only_fields: ClassVar = ['user_id', 'email', 'username', 'role', 'status', 'last_active', 'created_at', 'updated_at']

class UserSyncSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[]) ##to ignore email duplicate check
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'email', 'role']

    def validate_email(self, value):
        user_id = self.initial_data.get('user_id') #type: ignore
        existing = UserProfile.objects.filter(user_id=user_id).first()
        if existing is not None and existing.email != value:
            raise serializers.ValidationError('Email does not match existing record')
        return value


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['status']

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar =['role']

class UserLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'username', 'avatar']