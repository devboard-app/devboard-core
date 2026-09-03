from typing import ClassVar

from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'email', 'username', 'avatar', 'timezone', 'role', 'status', 'last_active', 'created_at', 'updated_at']
        read_only_fields: ClassVar = ['user_id', 'email', 'username', 'role', 'status', 'last_active', 'created_at', 'updated_at']


class UserLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields: ClassVar = ['user_id', 'username', 'avatar']




class UserSyncInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=UserProfile.Role.choices, required=False)

class UserProfileInputSerializer(serializers.Serializer):
    avatar = serializers.URLField(required=False, allow_blank=True)
    timezone = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("No fields to update.")
        return attrs

class UserStatusInputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=UserProfile.Status.choices)

class UserRoleInputSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=UserProfile.Role.choices)

class UserLookupInputSerializer(serializers.Serializer):
    usernames = serializers.ListField(child=serializers.CharField(), allow_empty=True)
