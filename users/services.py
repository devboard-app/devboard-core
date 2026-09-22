from rest_framework.exceptions import APIException, NotFound, ValidationError

from users.infrastructure import sync_user_role_to_auth, sync_user_status_to_auth

from .models import UserProfile
from .repository import create_user, get_user_by_email, get_user_by_id


class ProfileSaveException(APIException):
    status_code = 500
    default_detail = "Could not save the change. Please try again."


async def get_user_or_404(user_id: str) -> UserProfile:
    user = await get_user_by_id(user_id)
    if user is None:
        raise NotFound(detail="User not found")
    return user

async def get_user_by_email_or_404(email: str) -> UserProfile:
    user = await get_user_by_email(email)
    if user is None:
        raise NotFound(detail="User not found")
    return user

async def sync_user(user: UserProfile | None, data: dict) -> tuple [UserProfile, bool]:
    if user is None:
        user = await create_user(user_id=data['user_id'], email=data['email'], role=data.get('role', UserProfile.Role.MEMBER))
        return user, True
    if user.email != data['email']:
        raise ValidationError({'email': 'Email does not match existing user'})
    if 'role' in data:
        user.role = data['role']
        await user.asave(update_fields=['role', 'updated_at'])
    return user, False

async def update_profile(user: UserProfile, data: dict) -> UserProfile:
    for field, value in data.items():
        setattr(user, field, value)
    await user.asave(update_fields=[*data.keys(), 'updated_at'])
    return user

async def update_user_status(user: UserProfile, new_status: str) -> UserProfile:
    await sync_user_status_to_auth(str(user.user_id), new_status)
    user.status = new_status
    try:
        await user.asave(update_fields=['status', 'updated_at'])
    except Exception as exc:
        raise ProfileSaveException() from exc
    return user

async def update_user_role(user: UserProfile, new_role: str) -> UserProfile:
    await sync_user_role_to_auth(str(user.user_id), new_role)
    user.role = new_role
    try:
        await user.asave(update_fields=['role', 'updated_at'])
    except Exception as exc:
        raise ProfileSaveException() from exc
    return user