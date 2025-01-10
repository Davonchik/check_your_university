from pydantic import BaseModel

class AuthAdmin(BaseModel):
    email: str
    password: str

class AdminResponse(BaseModel):
    email: str
    access_token: str
    refresh_token: str
