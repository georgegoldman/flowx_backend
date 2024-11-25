from fastapi import APIRouter, Depends, HTTPException, status, Request
from flowx_backend.services.user import UserService
from flowx_backend.schemas.user import UserCreate, UserUpdate, UserResponse
from flowx_backend.core.dependencies import get_current_user

class UserAPI:
    
    def __init__(self) -> None:
        self.router = APIRouter()
        self.service = UserService("users")
        self.add_routes()

    def add_routes(self):
        self.router.post("/users/", response_model=UserResponse)(self.register_user)
        self.router.get("/users/{user_id}", response_model=UserResponse)(self.get_user)
        self.router.put("/users/{user_id}", response_model=UserResponse)(self.update_user_data)

    async def register_user(self, user_data: UserCreate):
        user = await self.service.createUser(user_data)
        return user
    
    async def get_user(self, user_id: str = Depends(get_current_user)):
        
        user = await self.service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    async def update_user_data(self, user_id: str , user_data: UserUpdate, current_user_id: str = Depends(get_current_user)):
        # Check if the user is trying to update their own data
        if current_user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this user")
        
        user = await self.service.update_user(user_id , user_data)
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    


user_api = UserAPI()

router = user_api.router