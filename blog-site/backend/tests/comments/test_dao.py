from tests.base_classes import BaseDAOTestCase
from tests.testdata.db_helper import insert_comment

from example_backend.comments import dao


class DAOTestCase(BaseDAOTestCase):
    def test_find_all_empty(self):
        result = dao.find_all()
        self.assertEqual([], result)

    def test_find_all(self):
        insert_comment()
        result = dao.find_all()
        self.assertEqual(1, len(result))
        self.assert_comment(result[0])

    def test_find(self):
        insert_comment()
        result = dao.find(1)
        self.assert_comment(result)

    def test_insert(self):
        result = dao.insert("title-1", "content-1", 1)
        self.assert_comment(result)

    def test_delete(self):
        insert_comment()
        dao.delete(1)
        self.assertIsNone(dao.find(1))

    def test_update(self):
        insert_comment()
        result = dao.update(1, "updated-content")
        self.assert_comment(result, "updated-content")

    def test_update_not_found(self):
        self.assertIsNone(dao.update(-1, ""))

    def assert_comment(self, comment, content="content-1"):
        self.assertEqual(1, comment.id)
        self.assertEqual(content, comment.content)
