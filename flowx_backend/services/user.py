from flowx_backend.schemas.user import UserResponse, UserCreate, UserLogin, UserUpdate
from flowx_backend.db.connection import get_collection
from bson import ObjectId
from flowx_backend.core.config import settings
from flowx_backend.core.jwt import  create_access_token, revoke_access_token
from flowx_backend.core.security import verify_password, hash_password
from bson.errors import InvalidId

collection = get_collection("users")

class UserService:

    def __init__(self, collection_name: str) -> None:
        self.collection = get_collection(collection_name)
    
    async def createUser(self, user_data:UserCreate) -> UserResponse:
        # Insert user into MongoDB and return UserResponse
        user_dict = user_data.model_dump()
        user_dict["password"] = hash_password(user_data.password)
        
        # Insert the user data into MongoDB
        result = await collection.insert_one(user_dict)

        # Return a UserResponse with the inserted ID
        return UserResponse(_id=str(result.inserted_id), **user_data.model_dump())


    async def get_user_by_id(self, user_id: str) -> UserResponse:
        try:
            # Ensure `user_id` is a valid ObjectId
            object_id = ObjectId(user_id)
        except (InvalidId, TypeError):
            raise ValueError(f"Invalid ObjectId: {user_id}")
        # Fetch a user by ID
        user = await collection.find_one({"_id": ObjectId(user_id) })
        
        return UserResponse(_id=str(object_id), username=user['username'], email=user["email"]) if user else None # type: ignore
    
    # Update a user by ID
    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserResponse | None:
        update_dict = user_data.model_dump(exclude_unset=True)
        if "password" in update_dict:
            update_dict["password"] = hash_password(update_dict["password"])  # Re-hash password if updating
        result = await collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_dict})
        if result.modified_count == 1:
            updated_user = await collection.find_one({"_id": ObjectId(user_id)})
            return UserResponse(_id=user_id, username=updated_user["username"], email=updated_user["email"]) if updated_user else None  # type: ignore
        return None
    
        # Delete a user by ID
    async def delete_user(self, user_id: str) -> bool:
        result = await collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count == 1

    async def authenticate_user(self, email: str, password: str) -> UserResponse | None:
        # Authenticate a user (dummy authentication for illustration)
        user = await collection.find_one({"email": email})

        # If the user exists and the password matches the hashed password, return UserResponse
        if user and verify_password(password, user["password"]) : # Assuming "password" is the hashed password field
            return UserResponse(_id=str(user["_id"]), **user)
        
        return None #type: ignore

    # Login user (returning JWT token)
    async def login_user(self, email: str, password: str) -> dict | None:
        user = await self.authenticate_user(email, password)
        if user:
            access_token = create_access_token({"sub": user.id})  # Assume user ID as subject
            return {"access_token": access_token, "token_type": "bearer"}
        return None

    # Logout user (token revocation)
    async def logout_user(self, token: str) -> bool:
        return revoke_access_token(token)  # Implement token revocation in JWT utility
    





