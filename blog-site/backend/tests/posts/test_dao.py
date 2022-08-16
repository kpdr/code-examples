from tests.base_classes import BaseDAOTestCase
from tests.testdata.db_helper import insert_post

from example_backend.posts import dao


class DAOTestCase(BaseDAOTestCase):
    def test_find_all_empty(self):
        result = dao.find_all()
        self.assertEqual([], result)

    def test_find_all(self):
        insert_post()
        result = dao.find_all()
        self.assertEqual(1, len(result))
        self.assert_post(result[0])

    def test_find(self):
        insert_post()
        result = dao.find(1)
        self.assert_post(result)

    def test_insert(self):
        result = dao.insert("title-1", "content-1", 1)
        self.assert_post(result)

    def test_delete(self):
        insert_post()
        dao.delete(1)
        self.assertIsNone(dao.find(1))

    def test_update(self):
        insert_post()
        result = dao.update(1, "updated-title", "updated-content")
        self.assert_post(result, "updated-title", "updated-content")

    def test_update_not_found(self):
        self.assertIsNone(dao.update(-1, "", ""))

    def assert_post(self, post, title="title-1", content="content-1"):
        self.assertEqual(1, post.id)
        self.assertEqual(title, post.title)
        self.assertEqual(content, post.content)
