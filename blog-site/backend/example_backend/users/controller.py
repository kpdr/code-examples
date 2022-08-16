from flask import Blueprint

from example_backend.extensions import as_json
from example_backend.users.service import auth_required

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("", methods=("POST",))
@auth_required(inject_user=True, inject_id_info=True)
@as_json
def create_or_verify_user(user, id_info):
    return {"user": user, "id_info": id_info}
