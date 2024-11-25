from fastapi import APIRouter
from flowx_backend.services.auth import AuthService
from flowx_backend.schemas.login_token import Token, LoginRequest

class AuthAPI:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.service = AuthService()
        self.add_routes()

    def add_routes(self):
        self.router.post("/auth/", response_model=Token)(self.login)

    async def login(self, request: LoginRequest):
        return await self.service.login(request.username, request.password)

auth_api = AuthAPI()
router = auth_api.router