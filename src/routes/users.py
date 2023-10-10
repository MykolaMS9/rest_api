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
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service dependency to get the current user.
    
    :param current_user: Users: Get the current user
    :return: The current user, which is passed to the function as a dependency
    :doc-author: ms
    """
    return current_user


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: Users = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function is used to update the avatar of a user.
        The function takes in an UploadFile object, which contains the file that will be uploaded to Cloudinary.
        It also takes in a Users object, which is the current_user who's avatar will be updated. 
        Finally it takes in a Session object, which is used for database transactions.
    
    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: Users: Get the current user's email from the database
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: ms
    """
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
