from datetime import datetime, timezone

from django.conf import settings
from jose import JWTError, jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import UserProfile


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try: 
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except JWTError:
            raise AuthenticationFailed('Invalid or expired token')

        user_id = payload.get('sub')
        if not user_id:
            raise AuthenticationFailed('Invalid token payload')

        user = UserProfile.objects.filter(user_id=user_id).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if user.status != UserProfile.Status.ACTIVE:
            raise AuthenticationFailed('User account is inactive')
        user.last_active = datetime.now(timezone.utc)
        user.save(update_fields=['last_active'])
        return (user, token)
        