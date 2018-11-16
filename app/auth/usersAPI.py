from flask import request, jsonify, current_app, make_response
from flask.views import MethodView

from app.auth.all_users import AllUsers
from app.auth.userTokens import UserToken
from app.auth.validations import verify_new_user_request_body
from app.exceptions import BadRequestError

class UsersAPI(MethodView):

    def __init__(self, logger=None, all_users=None, user_token=None):
        self.logger = logger or current_app.logger
        self.all_users = all_users or AllUsers(self.logger)
        self.user_token = user_token or UserToken()

    def post(self):
        try:
            request_body = request.get_json()
            verify_new_user_request_body(request_body, self.logger)

            new_user = self.all_users.add_one(request_body['last_name'], request_body['first_name'], request_body['email'],
                                         request_body['password'])
            user_id = new_user['user_id']
            auth_token = self.user_token.encode_auth_token(user_id)

            response_object = {
                'auth_token': auth_token.decode(),
                'user_id': user_id
            }
            return make_response(jsonify(response_object)), 201
        except BadRequestError as e:
            resp = jsonify({'code': 'ERR_BAD_REQUEST', 'message': e.message})
            self.logger.error('ERR_BAD_REQUEST EXCEPTION: ' + str(e))
            return make_response(resp), 400
        except Exception as e:
            self.logger.error('UNKNOWN EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_UNKNOWN', 'message': 'unknown error'})
            return make_response(resp), 500