from fastapi import APIRouter
from src.application.domain.request import RequestCreate, RequestOut, RequestUpdate
from src.factories import S3BucketServiceAnnotated
from fastapi import FastAPI, File, UploadFile
from typing import Annotated


s3_router = APIRouter(prefix="/s3", tags=["requests"])


@s3_router.post("/uploadfile/")
async def create_upload_file(file: UploadFile, s3: S3BucketServiceAnnotated):
    content = await file.read()
    filename = file.filename   
    s3.upload_file_object("image_report", filename, content)
    return "success"


@s3_router.get("/listfiles/")
async def list_files(s3: S3BucketServiceAnnotated):
    # доделать 
    return s3.list_objects("image_report")