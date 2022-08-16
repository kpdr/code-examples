from example_backend.extensions import db


def create_db():
    db.create_all()


def clear_db():
    db.drop_all()


def insert_user():
    db.engine.execute(
        "INSERT INTO users (id, email, name) VALUES (:id, :email, :name)",
        [{"id": 1, "email": "test@example.com", "name": "Test Name"}],
    )


def insert_post(user_id=1):
    db.engine.execute(
        "INSERT INTO Posts (id, title, content, user_id) VALUES (:post_id, :title, :content, :user_id)",
        [{"post_id": 1, "title": "title-1", "content": "content-1", "user_id": user_id}],
    )


def insert_comment(post_id=1, user_id=1):
    db.engine.execute(
        "INSERT INTO Comments (id, post_id, content, user_id) VALUES (:comment_id, :post_id, :content, :user_id)",
        [{"comment_id": 1, "post_id": post_id, "content": "content-1", "user_id": user_id}],
    )
