from flask import request, jsonify, current_app, make_response
from flask.views import MethodView

from app.auth.all_users import AllUsers
from app.auth.authorization import auth_token_required
from app.auth.userTokens import UserToken
from app.auth.validations import verify_new_user_request_body
from app.exceptions import BadRequestError

class OrdersApi(MethodView):

    def __init__(self):

        self.logger = current_app.logger
        self.all_users = AllUsers(self.logger)
        self.user_token = UserToken()

    def post(self):
        try:
            request_body = request.get_json()

            theorem_id = '123'
            response_object = {
                'theorem_id': theorem_id
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