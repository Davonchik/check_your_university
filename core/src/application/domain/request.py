from pydantic import BaseModel

class RequestCreate(BaseModel):
    building_name: str
    category: str
    room: str
    text: str
    photo_url: str

class RequestUpdate(BaseModel):
    status: str

class RequestOut(BaseModel):
    id: int
    user_id: int
    building_name: str
    category: str
    room: str
    text: str
    photo_url: str
    status: str