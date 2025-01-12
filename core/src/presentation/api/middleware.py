from jwt import PyJWTError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from src.infrastructure.utils.token_service import TokenService



class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, prefixes: list):
        super().__init__(app)
        self.prefixes = prefixes

    async def dispatch(self, request: Request, call_next):

        if request.url.path in ['/docs', '/openapi.json', '/redoc']:
            response = await call_next(request)
            return response

        if not any(request.url.path.startswith(prefix) for prefix in self.prefixes):
            response = await call_next(request)
            return response

        x_auth_token = request.headers.get('X-Auth-Token')

        if not x_auth_token:
            raise Exception('Missing X-Auth-Token')

        try:
            payload = await TokenService.decode_access_token(token=x_auth_token)
            request.state.user = payload

        except PyJWTError:
            raise Exception('Invalid X-Auth-Token')

        response = await call_next(request)
        return response