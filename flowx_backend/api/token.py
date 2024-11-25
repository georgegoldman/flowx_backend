from fastapi import APIRouter, HTTPException, Header, Depends, status
from fastapi.security import OAuth2PasswordBearer
from flowx_backend.schemas.token import TokenData, TokenRequest
from flowx_backend.services.token import TokenService
from typing import List
from flowx_backend.core.jwt import verify_jwt_with_fingerprint
from flowx_backend.core.dependencies import get_authenticated_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = TokenService("tokens")
        self.add_routes()
    
    def add_routes(self):
        self.router.post("/token/", response_model=TokenData)(self.create_token)
        self.router.get("/token/{token_id}", response_model=TokenData)(self.read_token)
        self.router.get("/token/", response_model=List[TokenData])(self.read_all_tokens)
        self.router.get("/token/device/{device_sig}", response_model=List[TokenData])(self.get_tokens_by_device_sig)
        self.router.delete("/tokens/{token_id}")(self.delete_token)
        self.router.get("/verify-token")(self.verify_token)

    async def create_token(self, request: TokenRequest, user_id: str = Depends(get_authenticated_user)):
        """Create a new token."""
        return await self.service.create_token(request.device_sig, request.name)

    async def read_token(self, token_id: str, user_id: str = Depends(get_authenticated_user)):
        """Get a specific token by ID."""
        return await self.service.get_token(token_id)
    
    async def read_all_tokens(self, user_id: str = Depends(get_authenticated_user)):
        """Retrieve all tokens."""
        return await self.service.get_all_tokens()
    
    async def get_tokens_by_device_sig(self, device_sig: str, user_id: str = Depends(get_authenticated_user)):
        """Get tokens by device signature."""
        return await self.service.get_tokens_by_device_sig(device_sig)
    
    async def delete_token(self, token_id: str, user_id: str = Depends(get_authenticated_user)):
        """Delete a token by ID."""
        return await self.service.delete_token_by_id(token_id)
    
    async def verify_token(self, short_token:str = Header(...), user_id: str = Depends(get_authenticated_user)):
        """Verify a short token."""
        hardware_fingerprint = await verify_jwt_with_fingerprint(short_token)
        return {"message": "Token verified successfully", "hardware_fingerprint": hardware_fingerprint}

# Instantiate the API and use its router
token_api = TokenAPI()

# Mount the router in the main app
router = token_api.router

