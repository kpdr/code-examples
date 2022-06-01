import http
from typing import List

import flask
from flask import jsonify, request

from example_backend.app import app
from example_backend.comments import dao
from example_backend.exc.bad_request import BadRequest
from example_backend.exc.not_found import NotFound
from example_backend.posts import dao as posts_dao


@app.route("/posts/<int:post_id>/comments", methods=("POST",))
def create(post_id):
    request_json = flask.request.json

    post = posts_dao.find(post_id)
    if not post:
        raise BadRequest("Could not find post")
    else:
        comment = dao.insert(post.id, request_json["content"])
        return comment_to_json(comment)


@app.route("/posts/<int:post_id>/comments", methods=("GET",))
def get_comments(post_id):
    post = posts_dao.find(post_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    return comments_to_json(post.comments)


@app.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=("GET",))
def get_comment(post_id, comment_id):
    post = posts_dao.find(post_id)
    comment = dao.find(comment_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    elif comment is None:
        raise NotFound(f"No comment found with id {comment_id}")
    return comment_to_json(comment)


@app.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=("PUT",))
def edit(post_id, comment_id):
    post = posts_dao.find(post_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    json_data = request.get_json()

    updated = dao.update(comment_id, json_data["content"])
    return comment_to_json(updated)


@app.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=("DELETE",))
def delete(post_id, comment_id):
    post = posts_dao.find(post_id)
    comment = dao.find(comment_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    elif comment is None:
        raise NotFound(f"No comment found with id {comment_id}")
    dao.delete(comment_id)
    return "", http.HTTPStatus.NO_CONTENT


def comment_to_json(comment: dao.Comments):
    return jsonify(comment.to_dict())


def comments_to_json(comments: List[dao.Comments]):
    return jsonify([comment.to_dict() for comment in comments])
