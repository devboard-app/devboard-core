from core.pagination import page

from .models import UserProfile


async def get_user_by_id(user_id: str)-> UserProfile | None:
    return await UserProfile.objects.filter(user_id=user_id).afirst()

async def get_user_by_email(email: str)-> UserProfile | None:
    return await UserProfile.objects.filter(email=email).afirst()

async def get_all_users(limit: int, offset: int)-> tuple[list[UserProfile], int]:
    return await page(UserProfile.objects.all(), limit, offset)

async def get_users_by_usernames(usernames: list[str]) -> list[UserProfile]:
    return [user async for user in UserProfile.objects.filter(username__in=usernames, status=UserProfile.Status.ACTIVE)]

async def get_users_by_ids(user_ids: list[str]) -> list[UserProfile]:
    return [user async for user in UserProfile.objects.filter(user_id__in=user_ids)]

async def create_user(user_id: str, email: str, role: UserProfile.Role) -> UserProfile:
    user = await UserProfile.objects.acreate(user_id=user_id, email=email, role=role)
    return user
