import httpx
from django.conf import settings
from rest_framework.exceptions import APIException


class AuthServiceException(APIException):
    status_code = 502
    default_detail = "Auth service is not working"

async def sync_user_status_to_auth(user_id: str, status: str) -> None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                f"{settings.AUTH_SERVICE_URL}/internal/users/{user_id}/status/",
                json={"is_active": status == "active"},
                headers={"X-Service-Key": settings.INTERNAL_API_KEY},
            )
            if response.status_code != 204:
                raise AuthServiceException()
        except httpx.RequestError:
            raise AuthServiceException()

async def sync_user_role_to_auth(user_id: str, role: str) -> None:
    async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(
                    f"{settings.AUTH_SERVICE_URL}/internal/users/{user_id}/role/",
                    json={"role": role},
                    headers={"X-Service-Key": settings.INTERNAL_API_KEY},
                )
                if response.status_code != 204:
                    raise AuthServiceException()
            except httpx.RequestError:
                raise AuthServiceException()