import time
from typing import TypedDict, ClassVar

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user.exceptions import NotAuthorizedException
from user.models import BlogUser


class JWTPayload(TypedDict):
    user_id: int
    exp: int


class AuthenticationService:
    JWT_SECRET_KEY: ClassVar[str] = settings.SECRET_KEY
    JWT_ALGORITHM: ClassVar[str] = "HS256"

    @staticmethod
    def _unix_timestamp(seconds_in_future: int) -> int:
        return int(time.time()) + seconds_in_future

    def encode_token(self, user_id: int) -> str:
        return jwt.encode(
            {
                "user_id": user_id,
                "exp": self._unix_timestamp(seconds_in_future=24 * 60 * 60),
            },
            self.JWT_SECRET_KEY,
            algorithm=self.JWT_ALGORITHM,
        )

    def verify_token(self, jwt_token: str) -> int:
        try:
            payload: JWTPayload = jwt.decode(
                jwt_token, self.JWT_SECRET_KEY, algorithms=[self.JWT_ALGORITHM]
            )
            user_id: int = payload["user_id"]
            exp: int = payload["exp"]
        except Exception:  # noqa
            raise NotAuthorizedException

        if exp < self._unix_timestamp(seconds_in_future=0):
            raise NotAuthorizedException
        return user_id


authentication_service = AuthenticationService()


class BearerAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split("Bearer ")[1]
        try:
            user_id: int = authentication_service.verify_token(jwt_token=token)
        except NotAuthorizedException:
            raise AuthenticationFailed("Invalid or missing token")

        user = BlogUser.objects.filter(id=user_id).first()
        if not user:
            raise AuthenticationFailed("User not found")

        # DRF는 튜플로 사용자와 인증 정보를 반환해야 함
        return user, token


bearer_auth = BearerAuth()