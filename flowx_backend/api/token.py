from fastapi import APIRouter, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from flowx_backend.schemas.token import TokenData, TokenRequest
from flowx_backend.services.token import create_token, get_token, get_all_tokens, get_tokens_by_device_sig, delete_token_by_id
from typing import List
from flowx_backend.core.jwt import verify_jwt_with_fingerprint


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create user (registration)
@router.post("/token/", response_model=TokenData)
async def register_user( request: TokenRequest):
    user = await create_token(request.device_sig)
    return user

@router.get("/token/{token_id}", response_model=TokenData)
async def read_token(token_id: str):
    token = await get_token(token_id)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token

@router.get("/token/", response_model=List[TokenData])
async def read_all_tokens():
    return await get_all_tokens()

@router.get("/token/device/{device_sig}", response_model=List[TokenData])
async def get_tokens(device_sig: str):
    return await get_tokens_by_device_sig(device_sig)

@router.delete("/tokens/{token_id}")
async def delete_token(token_id: str):
    return await delete_token_by_id(token_id)

@router.get("/verify-token")
async def verify_token(short_token: str = Header(...)):
    hardware_fingerprint = await verify_jwt_with_fingerprint(short_token)
    return {"message": "Token verified successfully", "hardware_fingerprint": hardware_fingerprint}