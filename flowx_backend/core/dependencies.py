from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from flowx_backend.core.security import verify_token
from flowx_backend.db.connection import get_collection
import ast

# OAuth2PasswordBearer extracts token from "Authorization: Bearer <token>"
oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify the token (from Authorization: Bearer <token>)
    try:
        payload = verify_token(token)
        payload_dict = ast.literal_eval(f"{payload}")
        usera_data = payload_dict
        if not usera_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},

            )
        # Return user data or object based on the payload
        return usera_data['sub']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception occurred: {str(e)}")

def get_user_collection():
    return get_collection("users")

async def get_authenticated_user(user_id: str = Depends(get_current_user)) -> str:
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user_id