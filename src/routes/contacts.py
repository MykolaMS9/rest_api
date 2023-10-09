from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.models import Users
from src.repository import contacts as repository_contacts
from src.database.db import get_db
from src.services.auth import auth_service
from src.schemas.contacts import ContactResponse, ContactModel

router = APIRouter(prefix='/contact', tags=['contact'])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db),
                       current_user: Users = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(limit, offset, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


# response_model=OwnerResponse,
@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: Users = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contact_by_id(contact_id, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: Users = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create(body, db, current_user.id)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: Users = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(contact_id, body, db, current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact}/name", response_model=List[ContactResponse],
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db),
                              current_user: Users = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contact_by_name(contact_name, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.patch("/{contact}/surname", response_model=List[ContactResponse],
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db),
                                 current_user: Users = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contact_by_surname(contact_surname, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.patch("/{contact}/email", response_model=ContactResponse, description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db),
                               current_user: Users = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db, current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact}/birthdays", response_model=List[ContactResponse],
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_nearly_birthdays(db: Session = Depends(get_db),
                                        current_user: Users = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_nearly_birthdays(db, current_user.id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: Users = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(contact_id, db, current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact
