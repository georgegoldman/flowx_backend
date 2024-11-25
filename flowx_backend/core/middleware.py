from typing import Awaitable, Callable
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import Response
from flowx_backend.core.security import get_current_user

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            # Extract Bearer token
            token = request.headers.get("Authorization").split(" ")[1] # type: ignore
            user  = await get_current_user(token) # Your function to decode and validate the JWT
            request.state.user = user # Attach the user to the request
        except Exception:
            request.state.user = None # If no user is found, set to None
        return await call_next(request)