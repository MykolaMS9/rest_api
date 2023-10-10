from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import Users
from src.schemas.users import UserModel


async def get_user_by_email(email: str, db: Session) -> Users | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.
    
    :param email: str: Pass in the email of the user
    :param db: Session: Pass the database session to the function
    :return: A user object if the email is found in the database
    :doc-author: ms
    """
    return db.query(Users).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object to be created.
            db (Session): The SQLAlchemy session object used for querying the database.
    
    :param body: UserModel: Get the data from the request body
    :param db: Session: Pass a database session to the function
    :return: The user object that was created
    :doc-author: ms
    """
    g = Gravatar(body.email)
    new_user = Users(username=body.username, email=body.email, password=body.password,
                     avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: Users, refresh_token, db: Session):
    """
    The update_token function updates the refresh token for a user in the database.
        Args:
            user (Users): The User object to update.
            refresh_token (str): The new refresh token to store in the database.
            db (Session): A connection to our PostgreSQL database.
    
    :param user: Users: Pass in the user object from the database
    :param refresh_token: Update the refresh token in the database
    :param db: Session: Pass the database session to the function
    :return: The user object
    :doc-author: ms
    """
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.
    
    
    :param email: str: Specify the email of the user that is being confirmed
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: ms
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url, db) -> Users:
    """
    The update_avatar function takes in an email and a url, then updates the avatar of the user with that email.
        Args:
            email (str): The user's unique identifier.
            url (str): The new URL for the avatar image.
    
    :param email: Find the user in the database
    :param url: Update the avatar url of a user
    :param db: Pass in the database connection to the function
    :return: A user object
    :doc-author: ms
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
