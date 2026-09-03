from rest_framework.exceptions import NotFound

from .models import UserProfile
from .repository import get_user_by_email, get_user_by_id


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