from fastapi import  HTTPException, status
from datetime import timedelta
from flowx_backend.core.security import authenticate_user, create_access_token
from flowx_backend.core.config import settings

class AuthService:
    def __init__(self) -> None:
        pass

    async def login(self, username, password):
        user = await authenticate_user(username, password)
        print(user)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": str(user["_id"]), "username":user["username"]}, expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAY))
        return {"access_token": access_token, "token_type": "bearer"}
    
