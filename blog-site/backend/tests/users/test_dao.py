from tests.base_classes import BaseDAOTestCase
from tests.testdata.db_helper import insert_user

from example_backend.users import dao


class DAOTestCase(BaseDAOTestCase):
    def test_insert(self):
        user = dao.insert("test@example.com", "Test Name")
        self.assert_user(user)

    def test_find(self):
        insert_user()
        user = dao.find(1)
        self.assert_user(user)

    def test_find_no_match(self):
        user = dao.find(1)
        self.assertIsNone(user)

    def test_find_by_email(self):
        insert_user()
        user = dao.find_by_email("test@example.com")
        self.assert_user(user)

    def test_find_by_email_no_match(self):
        user = dao.find_by_email("test@example.com")
        self.assertIsNone(user)

    def assert_user(self, user):
        self.assertEqual(1, user.id)
        self.assertEqual("test@example.com", user.email)
        self.assertEqual("Test Name", user.name)
        self.assertIsNotNone(user.created)
