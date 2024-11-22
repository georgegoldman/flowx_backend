from datetime import datetime, timedelta
from jose import jwt #type: ignore
from flowx_backend.core.config import settings
from flowx_backend.db.connection import collection
from fastapi import HTTPException
import hashlib

def generate_main_jwt(fingerprint:str):
    secret_key = settings.SECRET_KEY
    expiration_time = datetime.now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAY)

    # JWT payload
    payload = {
        'hardware_fingerprint': fingerprint,
        'iat': datetime.now(),
        'exp': expiration_time
    }

    # Generate the JWT
    jwt_token = jwt.encode(payload, secret_key, algorithm=settings.ALGORITHM)
    return jwt_token

def generate_32bit_key_for_jwt(jwt_token):
    # Generate a 32-character hash of the JWT
    hash_object = hashlib.sha256(jwt_token.encode())
    short_key = hash_object.hexdigest()[:32]
    return short_key

async def verify_jwt_with_fingerprint(short_token):
    secret_key = settings.SECRET_KEY
    algorithms = settings.ALGORITHM

    # Query the database to get the main_token using the short_token
    token_data = await collection.find_one({"short_token": short_token})
    if not token_data:
        raise HTTPException(status_code=404, detail="Token not found")
    
    main_token = token_data.get("main_token")
    if not main_token:
        raise HTTPException(status_code=500, detail="Main token missing in database")
    
    try:
        # Decode the main token
        decoded = jwt.decode(main_token, secret_key, algorithms)
        hardware_fingerprint = decoded.get('hardware_fingerprint')

        if not hardware_fingerprint:
            raise HTTPException(status_code=400, detail="Hardware fingerprint not found in main token")
        
        # Regenerate the short token from the main token
        expected_short_token = generate_32bit_key_for_jwt(main_token)

        # Compare the provided short token with the regenerated short token
        if short_token != expected_short_token:
            raise HTTPException(status_code=401, detail="Short token does not match main token")
        
        return hardware_fingerprint
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Main token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid main token")

