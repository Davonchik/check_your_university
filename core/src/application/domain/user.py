from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    tg_id: str

class UserOut(BaseModel):
    id: int
    tg_id: str