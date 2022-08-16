import unittest
from unittest.mock import MagicMock, patch

from example_backend.app import create_app
from example_backend.extensions import db
from example_backend.users.dao import User


class BaseAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("tests.settings")

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


class BaseDAOTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("tests.settings")

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()


class BaseControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("tests.settings")
        cls.client = cls.app.test_client()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.auth_user()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def auth_user():
        mock_resolver = MagicMock()
        mock_resolver.return_value = (User("fake email", "fake name"), {"fake": "id info"})
        patch("example_backend.users.service.resolve_user", mock_resolver).start()
