from tests.base_classes import BaseAppTestCase

from example_backend.exc.bad_request import BadRequest, handle_bad_request

BAD_REQ = BadRequest("unit test message", status_code=401, payload={"k1": "v1"})


class BadRequestTestCase(BaseAppTestCase):
    def test_to_dict(self):
        self.assertEqual("unit test message", BAD_REQ.message)
        self.assertEqual(401, BAD_REQ.status_code)
        self.assertEqual({"k1": "v1", "message": "unit test message"}, BAD_REQ.to_dict())

    def test_to_dict_default_status_code_no_payload(self):
        bad_req = BadRequest("unit test message")
        self.assertEqual("unit test message", bad_req.message)
        self.assertEqual(400, bad_req.status_code)
        self.assertEqual({"message": "unit test message"}, bad_req.to_dict())

    def test_handle_bad_request(self):
        response = handle_bad_request(BAD_REQ)
        self.assertEqual(BAD_REQ.status_code, response.status_code)
        self.assertEqual({"k1": "v1", "message": "unit test message"}, response.json)
