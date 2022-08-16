from tests.base_classes import BaseAppTestCase

from example_backend.exc.not_found import NotFound, handle_not_found

NOT_FOUND = NotFound("unit test message")


class NotFoundTestCase(BaseAppTestCase):
    def test_to_dict(self):
        self.assertEqual("unit test message", NOT_FOUND.message)
        self.assertEqual(404, NOT_FOUND.status_code)
        self.assertEqual({"message": "unit test message"}, NOT_FOUND.to_dict())

    def test_handle_not_found(self):
        response = handle_not_found(NOT_FOUND)
        self.assertEqual(NOT_FOUND.status_code, response.status_code)
        self.assertEqual({"message": "unit test message"}, response.json)
