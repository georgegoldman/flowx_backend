from datetime import datetime, timedelta
from jose import JWTError, jwt # type: ignore
from passlib.context import CryptContext # type: ignore
from flowx_backend.core.config import settings
from flowx_backend.db.connection import get_collection
from flowx_backend.schemas.user import UserResponse
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# OAuth2 Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT functions
def create_access_token(
        data: dict,
        expires_delta:
        timedelta = None #type: ignore
):
    print(data)
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAY))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return Exception("Invalid token") #type: ignore
    

async def get_user(username: str, from_collection: str):
    
    user = await collection(from_collection).find_one({"username": username})

    if not user:
        return None
    return user

async def authenticate_user(username: str, password: str):
    user = await get_user(username, "users")
    
    if not user or not verify_password( password, user["password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): #type: ignore  # noqa: F811
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAY))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user = get_user(username, "users")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


def collection(collection_name: str):
    return get_collection(collection_name)
