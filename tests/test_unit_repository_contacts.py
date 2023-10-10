import datetime
import unittest
from unittest.mock import MagicMock

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import and_

from src.database.models import Contact, Users
from src.repository.contacts import (
    get_contacts,
    get_contact_by_email,
    get_contact_by_id,
    get_contact_by_name,
    get_contact_by_surname,
    get_nearly_birthdays,
    create,
    update,
    remove
)
from src.schemas.contacts import ContactModel


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = Users(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, db=self.session, user_id=self.user.id)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().filter_by().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, db=self.session, user_id=self.user.id)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter_by().filter_by().first.return_value = None
        result = await get_contact_by_id(contact_id=1, db=self.session, user_id=self.user.id)
        self.assertIsNone(result)

    async def test_get_contact_by_name_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().filter_by().all.return_value = contacts
        result = await get_contact_by_name(name='Name', db=self.session, user_id=self.user.id)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_name_not_found(self):
        self.session.query().filter_by().filter_by().all.return_value = None
        result = await get_contact_by_name(name='Name', db=self.session, user_id=self.user.id)
        self.assertIsNone(result)

    async def test_get_contact_by_surname_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().filter_by().all.return_value = contacts
        result = await get_contact_by_surname(surname='Name', db=self.session, user_id=self.user.id)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_surname_not_found(self):
        self.session.query().filter_by().filter_by().all.return_value = None
        result = await get_contact_by_surname(surname='Name', db=self.session, user_id=self.user.id)
        self.assertIsNone(result)

    async def test_get_contact_by_email_found(self):
        contact = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().filter_by().first.return_value = contact
        result = await get_contact_by_email(email='Name', db=self.session, user_id=self.user.id)
        self.assertEqual(result, contact)

    async def test_get_contact_by_email_not_found(self):
        self.session.query().filter_by().filter_by().first.return_value = None
        result = await get_contact_by_email(email='Name', db=self.session, user_id=self.user.id)
        self.assertIsNone(result)

    async def test_get_nearly_birthdays(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().select_from().filter_by().filter().all.return_value = contacts
        result = await get_nearly_birthdays(db=self.session, user_id=self.user.id)
        self.assertEqual(result, contacts)

    async def test_create(self):
        body = ContactModel(
            id=1,
            name="name",
            surname="surname",
            phone="phone",
            email="email@gmail.com",
            birthday=datetime.datetime(day=1, month=1, year=2019),
            description="description",
            created_at=datetime.datetime(day=1, month=1, year=2019),
            updated_at=datetime.datetime(day=1, month=1, year=2019),
        )
        result = await create(body=body, db=self.session, user_id=self.user.id)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().filter_by().first.return_value = contact
        result = await remove(contact_id=1, user_id=self.user.id, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter_by().filter_by().first.return_value = None
        result = await remove(contact_id=1, user_id=self.user.id, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact = Contact()
        body = ContactModel(
            id=1,
            name="name",
            surname="surname",
            phone="phone",
            email="email@gmail.com",
            birthday=datetime.datetime(day=1, month=1, year=2019),
            description="description",
            created_at=datetime.datetime(day=1, month=1, year=2019),
            updated_at=datetime.datetime(day=1, month=1, year=2019),
        )
        self.session.query().filter_by().filter_by().first.return_value = contact
        result = await update(contact_id=1, body=body, user_id=self.user.id, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        contact = Contact()
        body = ContactModel(
            id=1,
            name="name",
            surname="surname",
            phone="phone",
            email="email@gmail.com",
            birthday=datetime.datetime(day=1, month=1, year=2019),
            description="description",
            created_at=datetime.datetime(day=1, month=1, year=2019),
            updated_at=datetime.datetime(day=1, month=1, year=2019),
        )
        self.session.query().filter_by().filter_by().first.return_value = None
        result = await update(contact_id=1, body=body, user_id=self.user.id, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
