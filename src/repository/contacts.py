from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import Contact
from src.schemas.contacts import ContactModel


async def get_contacts(limit: int, offset: int, db: Session, user_id: int):
    """
    The get_contacts function returns a list of contacts from the database.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before returning results
    :param db: Session: Pass the database session to the function
    :param user_id: int: Filter the contacts by user_id
    :return: A list of contacts
    """
    contacts = db.query(Contact).filter_by(user_id=user_id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session, user_id: int):
    """
    The get_contact_by_id function takes in a contact_id and user_id, then returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            db (Session): A database session to query from.
            user_id (int): The id of the User who owns this Contact object.

    :param contact_id: int: Specify the contact id of the contact we want to retrieve
    :param db: Session: Pass the database session to the function
    :param user_id: int: Filter the contacts by user_id
    :return: A contact object that matches the id and user_id passed in
    """
    contact = db.query(Contact).filter_by(id=contact_id).filter_by(user_id=user_id).first()
    return contact


async def get_contact_by_name(name: str, db: Session, user_id: int):
    """
    The get_contact_by_name function takes in a name and returns all contacts with that name.
        Args:
            name (str): The contact's first or last name.
            db (Session): A database session object to query the database for the contact.
            user_id (int): The id of the user who owns this contact, used to filter out other users' contacts from our results.

    :param name: str: Filter the contacts by name
    :param db: Session: Pass in the database session
    :param user_id: int: Filter the contacts by user_id
    :return: A list of contacts
    """
    contacts = db.query(Contact).filter_by(name=name).filter_by(user_id=user_id).all()
    return contacts


async def get_contact_by_surname(surname: str, db: Session, user_id: int):
    """
    The get_contact_by_surname function returns a list of contacts with the given surname.


    :param surname: str: Filter the contacts by surname
    :param db: Session: Pass the database session to the function
    :param user_id: int: Filter the contacts by user_id
    :return: A list of contacts with the given surname
    """
    contacts = db.query(Contact).filter_by(surname=surname).filter_by(user_id=user_id).all()
    return contacts


async def get_contact_by_email(email: str, db: Session, user_id: int):
    """
    The get_contact_by_email function takes in an email and a user_id,
        then returns the contact associated with that email.

    :param email: str: Pass in the email address of the contact we want to retrieve
    :param db: Session: Pass in a database session object
    :param user_id: int: Filter the contact by user_id
    :return: The contact with the specified email address
    """
    contact = db.query(Contact).filter_by(email=email).filter_by(user_id=user_id).first()
    return contact


async def get_nearly_birthdays(db: Session, user_id: int):
    """
    The get_nearly_birthdays function returns a list of contacts whose birthdays are within 7 days from the current date.


    :param db: Session: Connect to the database
    :param user_id: int: Filter the contacts by user_id
    :return: All contacts that have a birthday in the next 7 days
    """
    contact = db.query(Contact) \
        .select_from(Contact) \
        .filter_by(user_id=user_id) \
        .filter(and_(func.date_part('day', Contact.birthday) - func.date_part('day', func.current_date()) <= 7,
                     func.date_part('month', Contact.birthday) == func.date_part('month', func.current_date()))) \
        .all()
    return contact


async def create(body: ContactModel, db: Session, user_id: int):
    """
    The create function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            db (Session): A connection to the database.

    :param body: ContactModel: Pass the data from the request body
    :param db: Session: Access the database
    :param user_id: int: Get the user_id from the token
    :return: The contact object
    """
    contact = Contact(name=body.name, surname=body.surname, phone=body.phone, \
                      email=body.email, birthday=body.birthday, description=body.description, user_id=user_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session, user_id: int):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated version of the ContactModel object.

    :param contact_id: int: Identify the contact to be deleted
    :param body: ContactModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :param user_id: int: Check if the contact belongs to the user
    :return: The contact object
    """
    contact = await get_contact_by_id(contact_id, db, user_id)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.surname = body.surname
        contact.birthday = body.birthday
        contact.description = body.description
        contact.user_id = user_id
        db.commit()
    return contact


async def remove(contact_id: int, db: Session, user_id: int):
    """
    The remove function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be deleted.
            db (Session): A connection to the database.
            user_id (int): The id of the user who owns this contact.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param user_id: int: Check if the contact belongs to the user
    :return: The contact that was removed
    """
    contact = await get_contact_by_id(contact_id, db, user_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
