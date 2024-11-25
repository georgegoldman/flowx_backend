from pydantic import BaseModel

class Token(BaseModel):
    name: str
    main_token: str
    short_token:str

class TokenData(Token):
    id: str

class TokenCreate(Token):
    device_sig: str

class TokenRequest(BaseModel):
    device_sig: str
    name: str