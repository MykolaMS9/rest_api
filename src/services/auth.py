from datetime import datetime, timedelta
import pickle
from typing import Optional

import redis
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.conf.config import settings
from src.database.db import get_db
from src.repository import users as repository_users


class ConfigKey:
    SECRET_KEY = settings.secret_key_jwt
    ALGORITHM = settings.algorithm


class Token:
    config = ConfigKey

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token.
            Args:
                data (dict): A dictionary of key-value pairs to include in the payload of the JWT.
                expires_delta (Optional[float]): An optional timedelta object that represents how long this token should last.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded in the token
        :param expires_delta: Optional[float]: Define the time in seconds that the token will expire
        :return: A token that is encoded with the data passed to it
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_access_token

        # define a function to generate a new refresh token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of seconds until the refresh token expires. Defaults to None, which sets it to 7 days from now.

        :param self: Access the class attributes and methods
        :param data: dict: Pass the user's id and username to the function
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: The encoded refresh token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
        It takes a refresh_token as an argument and returns the email of the user if successful.
        If it fails, it raises an HTTPException with status code 401 (UNAUTHORIZED) and detail message.

        :param self: Represent the instance of the class
        :param refresh_token: str: Decode the refresh token
        :return: The email of the user who is trying to refresh their token
        """
        try:
            payload = jwt.decode(refresh_token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    def create_email_token(self, data: dict):
        """
        The create_email_token function takes a dictionary of data and returns a JWT token.
        The token is encoded with the SECRET_KEY and ALGORITHM from the config file.
        The expiration date for this token is set to 7 days from now.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded into the token
        :return: A token that is encoded using jwt
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function uses PyJWT to decode the JWT, which is then used to retrieve the email address from its payload.

        :param self: Represent the instance of the class
        :param token: str: Get the token from the request
        :return: The email that is stored in the token
        """
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


class Auth(Token):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def __init__(self):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the configuration for our application, and initializes a password hashing context.

        :param self: Represent the instance of the class
        :return: The config and pwd_context
        """
        self.config = ConfigKey
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. It then uses the pwd_context object to verify that the
        plain-text password matches the hashed one.

        :param self: Make the function a method of the class
        :param plain_password: Pass in the password that is being verified
        :param hashed_password: Store the hashed password in the database
        :return: A boolean value
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
        The hash is generated using the pwd_context object, which is an instance of Flask-Bcrypt's Bcrypt class.

        :param self: Make the function a method of the user class
        :param password: str: Get the password from the user
        :return: A hash of the password that can be stored in the database
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            UserRouter class. It takes in a token and db session, and returns the user
            object associated with that token. If no user is found, it raises an exception.

        :param self: Access the class variables and methods
        :param token: str: Get the token from the authorization header
        :param db: Session: Get the database session
        :return: The user object
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            if payload.get('scope') == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user


auth_service = Auth()
