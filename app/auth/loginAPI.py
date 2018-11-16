from flask import request, jsonify, current_app, make_response
from flask.views import MethodView

from app.auth.authorization import auth_token_required
from app.auth.userTokens import  UserToken
from app.exceptions import BadRequestError, NonExistentError
from app.auth.all_users import AllUsers
from app.auth.validations import verify_login_request_body

class LoginAPI(MethodView):

    def __init__(self):

        self.logger = current_app.logger
        self.all_users = AllUsers(self.logger)
        self.user_token = UserToken()

    def post(self):
        try:
            request_body = request.get_json()
            verify_login_request_body(request_body, self.logger)
            user = self.all_users.fetch_one_by_email_and_password(request_body['email'],request_body['password'])
            if not user:
                raise NonExistentError('Password and Email do not match')
            user_id = user['id']
            auth_token = self.user_token.encode_auth_token(user_id)
            response_object = {
                'user_id' : user_id,
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(response_object)), 200
        except BadRequestError as e:
            self.logger.error('ERR_BAD_REQUEST EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_BAD_REQUEST', 'message': e.message})
            return make_response(resp), 400
        except NonExistentError as e:
            self.logger.error('ERR_UNAUTHORISED EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_UNAUTHORISED', 'message': e.message})
            return make_response(resp), 401
        except Exception as e:
            self.logger.error('UNKNOWN EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_UNKNOWN', 'message': 'unknown error'})
            return make_response(resp), 500
