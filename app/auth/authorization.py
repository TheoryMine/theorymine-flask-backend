from functools import wraps
from flask import request, current_app, jsonify, make_response

from app.auth.userTokens import UserToken
from app.exceptions import UnauthorisedError


def auth_token_required(func):
    @wraps(func)
    def auth_decorator(*args, **kwargs):
        try:
            logger = current_app.logger
            user_token = UserToken()
            logger.info('Authorising user with basic auth')
            auth_header = request.headers.get('Authorization')
            auth_token_split = auth_header and auth_header.split(" ")
            auth_token = auth_token_split and len(auth_token_split) >1 and auth_token_split[1]
            if auth_token:
                user_id = user_token.decode_auth_token(auth_token)
                new_args = [*args, user_id]
                return func(*new_args, **kwargs)
            else:
                raise UnauthorisedError('Please provide an auth token')
        except UnauthorisedError as e:
            resp = jsonify({'code': 'ERR_UNAUTHORISED_REQUEST', 'message': e.message})
            logger.error('ERR_UNAUTHORISED_REQUEST EXCEPTION: ' + str(e))
            return make_response(resp), 401
    return auth_decorator

