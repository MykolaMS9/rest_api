from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import Users
from src.schemas.users import UserModel


async def get_user_by_email(email: str, db: Session) -> Users | None:
    return db.query(Users).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    g = Gravatar(body.email)
    new_user = Users(username=body.username, email=body.email, password=body.password,
                     avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: Users, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url, db) -> Users:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
