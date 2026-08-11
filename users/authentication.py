from asgiref.sync import async_to_sync
from django.conf import settings
from jose import JWTError, jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .repository import get_user_by_id


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

        user = async_to_sync(get_user_by_id)(user_id)
        if user is None:
            raise AuthenticationFailed('User not found')

        return (user, token)
        