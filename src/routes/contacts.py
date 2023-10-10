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
    """
    The get_contacts function returns a list of contacts.
    
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the maximum number of contacts returned
    :param offset: int: Specify the starting point of the query
    :param db: Session: Get the database session
    :param current_user: Users: Get the current user
    :return: A list of contacts
    :doc-author: ms
    """
    contacts = await repository_contacts.get_contacts(limit, offset, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


# response_model=OwnerResponse,
@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: Users = Depends(auth_service.get_current_user)):
    """
    The get_contact function is used to retrieve a single contact from the database.
    The function takes in an integer value for the contact_id, which is then passed into
    the get_contact_by_id function of repository/contacts.py. The get_contact function returns
    a JSON object containing all information about a specific contact.
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get the database session
    :param current_user: Users: Get the user id of the current user
    :return: A contact object
    :doc-author: ms
    """
    contacts = await repository_contacts.get_contact_by_id(contact_id, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: Users = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactModel: Get the data from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: Users: Get the user_id from the current user
    :return: A contactmodel object
    :doc-author: ms
    """
    contact = await repository_contacts.create(body, db, current_user.id)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: Users = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and db as parameters.
        It returns a ContactModel object.
    
    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Specify the id of the contact to update
    :param db: Session: Get the database session
    :param current_user: Users: Get the current user from the database
    :return: A contactmodel object
    :doc-author: ms
    """
    contact = await repository_contacts.update(contact_id, body, db, current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact}/name", response_model=List[ContactResponse],
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db),
                              current_user: Users = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_name function is used to retrieve a contact by name.
        The function takes in the following parameters:
            - contact_name (str): The name of the contact you wish to retrieve.
            - db (Session, optional): A database Session instance that will be used for querying data from the database.  Defaults to Depends(get_db).
            - current_user (Users, optional): An instance of Users representing the currently logged-in user.  Defaults to Depends(auth_service.get_current_user).
    
    :param contact_name: str: Get the contact name from the url
    :param db: Session: Get the database session
    :param current_user: Users: Get the current user's id
    :return: A list of contacts
    :doc-author: ms
    """
    contacts = await repository_contacts.get_contact_by_name(contact_name, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.patch("/{contact}/surname", response_model=List[ContactResponse],
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db),
                                 current_user: Users = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_surname function is used to retrieve a contact by surname.
        The function takes in the following parameters:
            - contact_surname (str): The surname of the contact you wish to retrieve.
            - db (Session, optional): A database Session instance that will be used for querying data from the database. 
                Defaults to None if not provided. If no value is provided, a new Session instance will be created and used instead. 
                This parameter should only be set when testing this function as it allows us to mock out our database connection for testing purposes.
    
    :param contact_surname: str: Pass the surname of the contact to be searched for
    :param db: Session: Pass the database session to the function
    :param current_user: Users: Get the current user
    :return: A list of contacts with the given surname
    :doc-author: ms
    """
    contacts = await repository_contacts.get_contact_by_surname(contact_surname, db, current_user.id)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.patch("/{contact}/email", response_model=ContactResponse, description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db),
                               current_user: Users = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_email function returns a contact by email.
        The function takes in the following parameters:
            - contact_email (str): The email of the contact to be returned.
            - db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            - current_user (Users, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_email: str: Specify the email of the contact to be retrieved
    :param db: Session: Get the database session
    :param current_user: Users: Get the current user
    :return: A contact object
    :doc-author: ms
    """
    contact = await repository_contacts.get_contact_by_email(contact_email, db, current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact}/birthdays", response_model=List[ContactResponse],
              description='No more than 10 requests per minute',
              dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_nearly_birthdays(db: Session = Depends(get_db),
                                        current_user: Users = Depends(auth_service.get_current_user)):
    """
    The get_contacts_nearly_birthdays function returns a list of contacts that have birthdays in the next 30 days.
    
    :param db: Session: Get the database session
    :param current_user: Users: Get the current user
    :return: A list of contacts with birthdays in the next 7 days
    :doc-author: ms
    """
    contact = await repository_contacts.get_nearly_birthdays(db, current_user.id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: Users = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
        The function takes in an integer as a parameter, which is the ID of the contact to be deleted.
        It also takes in two dependencies: db and current_user. 
            - db is used to access our database session, so we can make changes to it (in this case deleting). 
            - current_user is used for authentication purposes; only users who are logged into their account can delete contacts.
    
    :param contact_id: int: Specify the id of the contact to delete
    :param db: Session: Get the database session
    :param current_user: Users: Get the user id of the currently logged in user
    :return: The deleted contact
    :doc-author: ms
    """
    contact = await repository_contacts.remove(contact_id, db, current_user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact
