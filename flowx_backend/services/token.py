from flowx_backend.schemas.token import TokenCreate, TokenData
from flowx_backend.db.connection import  get_collection
from bson import ObjectId
from flowx_backend.core.jwt import generate_32bit_key_for_jwt, generate_main_jwt
from typing import List
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException



class TokenService:
    def __init__(self, collection_name: str) -> None:
        self.collection = get_collection(collection_name)

    async def create_token(self, device_sig: str, name:str) -> TokenData:
        # Generate main and short tokens
        main_token = generate_main_jwt(device_sig)
        short_token = generate_32bit_key_for_jwt(main_token)
        
        # Prepare token data
        token_data = TokenCreate(
            main_token=main_token,
            short_token=short_token,
            device_sig=device_sig,
            name=name
        )

        try:
            # Insert the token data into MongoDB
            await self.collection.insert_one(token_data.model_dump())
        except DuplicateKeyError:
            # Handle the case where the device_sig (used as _id) already exists
            raise HTTPException(status_code=400, detail="Token with this device_sig already exists")
        
        # Retrieve the document using device_sig
        created_doc = await self.collection.find_one({"short_token": short_token})

        if not created_doc:
            # Handle the case where the document is not found
            raise HTTPException(status_code=500, detail="Failed to retrieve the created document")

        # Map the retrieved document to your response class
        return TokenData(
                short_token=created_doc["short_token"], 
                id=str(created_doc["_id"]), 
                main_token=created_doc["main_token"],
                name=created_doc["name"]
            )

    async def get_token(self, token_id: str) -> TokenData:
        # Ensure the token_id is a valid ObjectId
        if not ObjectId.is_valid(token_id):
            raise HTTPException(status_code=400, detail="Invalid token ID format")
        
        # Find the document by _id
        token = await self.collection.find_one({"_id": ObjectId(token_id)})

        if not token:
            # Raise an exception if the token is not found
            raise HTTPException(status_code=404, detail="Token not found")
        
        # Map the MongoDB document to the TokenData model
        return TokenData(
            short_token=token["short_token"],
            id=str(token["_id"]), # Convert ObjectId to string
            main_token=token["main_token"],
            name=token["name"]
        )
    
    async def get_all_tokens(self) -> List[TokenData]:
        # Retrieve all documents from the collection
        cursor = self.collection.find() # Return a cursor object for all documents
        tokens  = await cursor.to_list(length=None) # Convert cursor to a list (length=None means fetch all)
        
        # Map each document to the TokenData model
        return [
            TokenData(
                short_token=token["short_token"],
                id=str(token["_id"]), # convert ObjectId to string
                main_token=token["main_token"],
                name=token["name"]
            )
            for token in tokens # use 'token' here as the iterable variable
        ]

    async def get_tokens_by_device_sig(self, device_sig: str) -> List[TokenData]:
        # Find all documents matching the device_sig
        token_cursor = self.collection.find({"device_sig": device_sig})

        # Convert the cursor to a list
        tokens = await token_cursor.to_list(length=None)

        if not tokens:
            # Raise an exception if no tokens are found
            raise HTTPException(status_code=404, detail="No tokens found for this device_sig")
        
        # Map the MongoDB documents to the TokenData model
        return [
            TokenData(
                short_token=token["short_token"],
                id=str(token["_id"]),
                main_token=token["main_token"],
                name=token["name"]
            )
            for token in tokens
        ]

    # Delete a user by ID
    async def delete_token_by_id(self, token_id: str):

        #Validate and convert the token_id to an ObjectId
        try:
            token_id_obj = ObjectId(token_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token ID format")
        
        # Delete the document
        result = await self.collection.delete_one({"_id": token_id_obj})

        if result.deleted_count == 0:
            # Raise an exception if no document was deleted
            raise HTTPException(status_code=404, detail="Token not found")
        
        return {"detail": "Token deleted successfuly"}
    # Implement token revocation in JWT utility