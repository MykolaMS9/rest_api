from sqlalchemy.orm import Session
from fastapi import File, UploadFile

import cloudinary
import cloudinary.uploader

from src.conf.config import settings
from src.database.db import get_db
from src.database.models import Users
from src.repository import users as repository_users
from src.schemas.users import UserResponse
from fastapi import Depends, APIRouter

from src.services.auth import auth_service

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Users = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: Users = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    public_id = f'ContactsApp/{current_user.username}{current_user.id}'
    r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    src_url = cloudinary.CloudinaryImage(public_id) \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
