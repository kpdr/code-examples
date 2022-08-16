from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from example_backend.extensions import db


class Posts(db.Model, SerializerMixin):
    __tablename__ = "posts"

    serialize_only = ("id", "created", "title", "content", "comments", "user.id", "user.name")

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User")
    title = db.Column(db.String())
    content = db.Column(db.String())
    comments = db.relationship("Comments", backref="post")

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id


def insert(title, content, user_id):
    post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return post


def find(post_id):
    return db.session.query(Posts).get(post_id)


def find_all():
    return db.session.query(Posts).all()


def delete(post_id):
    post = find(post_id)
    db.session.delete(post)
    db.session.commit()


def update(post_id, title, content):
    post = find(post_id)
    if not post:
        return None

    post.title = title
    post.content = content
    db.session.commit()
    return post
