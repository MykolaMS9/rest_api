from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    description: str
    created_at: datetime
    updated_at: datetime


class ContactResponse(BaseModel):
    id: int = 1
    name: str = Field(min_length=1, max_length=30)
    surname: str = Field(min_length=1, max_length=30)
    email: EmailStr
    phone: str = Field(min_length=1, max_length=30)
    birthday: date
    description: str
    created_at: datetime
    updated_at: datetime

    # Якщо поветраються з бази даних
    class Config:
        from_attributes = True
