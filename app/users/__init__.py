from flask import Blueprint, request, jsonify, current_app
import hashlib

from app.exceptions import BadRequestError
from app.users.all_users import AllUsers

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/users', methods=['POST'])
def users():
    logger = current_app.logger
    all_users = AllUsers(logger)

    if request.method == 'POST':
        try:
            request_body = request.get_json()
            new_user = all_users.add_one(request_body['last_name'], request_body['first_name'], request_body['email'],
                                         request_body['password'])
            resp = jsonify(new_user)
            resp.status_code = 201
            return resp
        except BadRequestError as e:
            resp = jsonify({'code': 'ERR_BAD_REQUEST', 'message': e.message})
            resp.status_code = 400
            return resp
        except Exception as e:
            logger.error('UNKNOWN EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_UNKNOWN', 'message': 'unknown error'})
            resp.status_code = 500
            return resp
