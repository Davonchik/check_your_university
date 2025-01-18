from fastapi import APIRouter, Form, File
from src.application.domain.request import RequestCreate, RequestOut, RequestUpdate
from src.factories import RequestServiceAnnotated, S3ServiceAnnotated
from fastapi import UploadFile

router_request = APIRouter(prefix="/request", tags=["requests"])

@router_request.post('/')
async def create_new_request(
    service: RequestServiceAnnotated,
    s3: S3ServiceAnnotated,
    user_id: int = Form(...),
    building_name: str = Form(...),
    category: str = Form(...),
    room: str = Form(...),
    text: str = Form(...),
    file: UploadFile = File(...)
):
    print("get request")
    read_file = await file.read()
    await s3.create_file("image_report", file.filename, read_file)
    return await service.create_request(RequestCreate(user_id=user_id, building_name=building_name, category=category, room=room, text=text))
