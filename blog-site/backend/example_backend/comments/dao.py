from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from example_backend.extensions import db


class Comments(db.Model, SerializerMixin):
    __tablename__ = "comments"

    serialize_only = ("id", "created", "post_id", "content", "user.id", "user.name")

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User")
    content = db.Column(db.String())

    def __init__(self, post_id, content, user_id):
        self.post_id = post_id
        self.content = content
        self.user_id = user_id


def insert(post_id, content, user_id):
    comment = Comments(post_id=post_id, content=content, user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return comment


def find(comment_id) -> Comments:
    return db.session.query(Comments).get(comment_id)


def find_all():
    return db.session.query(Comments).all()


def delete(comment_id):
    comment = find(comment_id)
    if not comment:
        return None
    db.session.delete(comment)
    db.session.commit()


def update(comment_id, content):
    comment = find(comment_id)
    if not comment:
        return None

    comment.content = content
    db.session.commit()
    return comment
