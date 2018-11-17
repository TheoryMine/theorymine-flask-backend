from flask import request, jsonify, current_app, make_response
from flask.views import MethodView

from app.auth.all_users import AllUsers
from app.auth.authorization import auth_token_required
from app.auth.userTokens import UserToken
from app.exceptions import BadRequestError, UnauthorisedError, StripeCardError
from app.registry.StripePayments import StripePayments
from app.registry.all_orders import AllOrders
from app.registry.validations import verify_orders_request_body


class OrdersApi(MethodView):

    def __init__(self):

        self.logger = current_app.logger
        self.all_users = AllUsers(self.logger)
        self.all_orders = AllOrders(self.logger)
        self.user_token = UserToken()
        self.stripe_payments = StripePayments()

    @auth_token_required
    def post(self, user_id):
        try:
            request_body = request.get_json()
            verify_orders_request_body(request_body, self.logger)
            theorem_name = request_body['theorem_name']
            payment_token = request_body['payment_token']
            theorem_id = self.all_orders.add_one(user_id, order_name = theorem_name)
            self.stripe_payments.charge_customer(payment_token = payment_token, theorem_name = theorem_name)
            response_object = {'theorem_id': theorem_id}
            return make_response(jsonify(response_object)), 201
        except BadRequestError as e:
            resp = jsonify({'code': 'ERR_BAD_REQUEST', 'message': e.message})
            self.logger.error('ERR_BAD_REQUEST EXCEPTION: ' + str(e))
            return make_response(resp), 400
        except UnauthorisedError as e:
            resp = jsonify({'code': 'ERR_UNAUTHORISED_REQUEST', 'message': e.message})
            self.logger.error('ERR_UNAUTHORISED_REQUEST EXCEPTION: ' + str(e))
            return make_response(resp), 404
        except StripeCardError as e:
            resp = jsonify({'code': 'ERR_PAYMENT', 'message': e.message})
            self.logger.error('ERR_PAYMENT EXCEPTION: ' + str(e))
            return make_response(resp), 500
        except Exception as e:
            self.logger.error('UNKNOWN EXCEPTION: ' + str(e))
            resp = jsonify({'code': 'ERR_UNKNOWN', 'message': 'unknown error'})
            return make_response(resp), 500