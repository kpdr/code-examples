import http

import flask
from flask import Blueprint, request

from example_backend.comments import dao
from example_backend.exc.bad_request import BadRequest
from example_backend.exc.not_found import NotFound
from example_backend.extensions import as_json
from example_backend.posts import dao as posts_dao
from example_backend.users.service import auth_required

blueprint = Blueprint("comment", __name__, url_prefix="/posts/<int:post_id>/comments")


@blueprint.route("", methods=("POST",))
@auth_required(inject_user=True)
@as_json
def create(post_id, user):
    request_json = flask.request.json

    post = posts_dao.find(post_id)
    if not post:
        raise BadRequest("Could not find post")
    else:
        return dao.insert(post.id, request_json["content"], user.id)


@blueprint.route("", methods=("GET",))
@as_json
def get_comments(post_id):
    post = posts_dao.find(post_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    return post.comments


@blueprint.route("/<int:comment_id>", methods=("GET",))
@as_json
def get_comment(post_id, comment_id):
    post = posts_dao.find(post_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    comment = dao.find(comment_id)
    if comment is None:
        raise NotFound(f"No comment found with id {comment_id}")
    return comment


@blueprint.route("/<int:comment_id>", methods=("PUT",))
@auth_required()
@as_json
def edit(post_id, comment_id):
    post = posts_dao.find(post_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    json_data = request.get_json()

    return dao.update(comment_id, json_data["content"])


@blueprint.route("/<int:comment_id>", methods=("DELETE",))
@auth_required()
def delete(post_id, comment_id):
    post = posts_dao.find(post_id)
    comment = dao.find(comment_id)
    if post is None:
        raise NotFound(f"No post found with id {post_id}")
    if comment is None:
        raise NotFound(f"No comment found with id {comment_id}")
    dao.delete(comment_id)
    return "", http.HTTPStatus.NO_CONTENT
