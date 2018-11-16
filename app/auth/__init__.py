from flask import Blueprint, request, jsonify, current_app

from app.exceptions import BadRequestError, NonExistentError
from app.auth.all_users import AllUsers
from app.auth.validations import verify_new_user_request_body

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/users', methods=['POST'])
def users():
    logger = current_app.logger
    all_users = AllUsers(logger)

    if request.method == 'POST':
        try:
            request_body = request.get_json()
            verify_new_user_request_body(request_body, logger)

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
            return resp@bp.route('/users', methods=['POST'])

@bp.route('/session', methods=['POST'])
def session():
    logger = current_app.logger
    all_users = AllUsers(logger)

    if request.method == 'POST':
        try:
            request_body = request.get_json()
            new_user = all_users.fetch_one_by_email_and_password(request_body['email'],request_body['password'])
            if not new_user:
                raise NonExistentError('Password and Email do not match')
            resp = jsonify({})
            resp.status_code = 200
            return resp
        except BadRequestError as e:
            resp = jsonify({'code': 'ERR_BAD_REQUEST', 'message': e.message})
            resp.status_code = 400
            return resp
        except NonExistentError as e:
            resp = jsonify({'code': 'ERR_UNAUTHORISED', 'message': e.message})
            resp.status_code = 401
            return resp
        except Exception as e:
            logger.error('UNKNOWN EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_UNKNOWN', 'message': 'unknown error'})
            resp.status_code = 500
            return resp
