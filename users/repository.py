from datetime import datetime, timezone

from .models import UserProfile


async def get_user_by_id(user_id: str)-> UserProfile | None:
    return await UserProfile.objects.filter(user_id=user_id).afirst()

async def get_user_by_email(email: str)-> UserProfile | None:
    return await UserProfile.objects.filter(email=email).afirst()

async def update_last_active(user: UserProfile) -> None:
    user.last_active = datetime.now(timezone.utc)
    await user.asave(update_fields=['last_active'])