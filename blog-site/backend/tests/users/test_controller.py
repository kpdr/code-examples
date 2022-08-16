from unittest.mock import patch

from tests.base_classes import BaseControllerTestCase

from example_backend.exc.bad_request import BadRequest


class UsersControllerTestCase(BaseControllerTestCase):
    @patch("example_backend.users.service.resolve_user", side_effect=BadRequest("bad token"))
    def test_create_or_verify_user_fails(self, mock_resolve_user):
        with self.client as c:
            response = c.post("/users", headers={"Authorization": "Bearer bad-token"})
            self.assertEqual(400, response.status_code)
            self.assertEqual("bad token", response.get_json()["message"])
            mock_resolve_user.assert_called_once()

    def test_create_or_verify_user_succeeds(self):
        with self.client as c:
            response_json = c.post("/users").get_json()
            self.assertEqual(
                {"email": "fake email", "name": "fake name", "id": None, "created": None}, response_json["user"]
            )
            self.assertEqual({"fake": "id info"}, response_json["id_info"])
