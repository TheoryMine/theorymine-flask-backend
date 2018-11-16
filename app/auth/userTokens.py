import jwt
import datetime
from flask import current_app

from app.auth.all_users import AllUsers
from app.exceptions import UnauthorisedError


class UserToken:

    def __init__(self):
        self.secret_key = current_app.config.get('SECRET_KEY')
        self.logger = current_app.logger
        self.all_users = AllUsers(self.logger)

    def encode_auth_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + current_app.config.get('SESSION_LENGTH'),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret_key ,
            algorithm='HS256'
        )

    def decode_auth_token(self, auth_token):
        try:
            decoded_token = jwt.decode(auth_token, self.secret_key )
            user_id = decoded_token['sub']
            return user_id
        except jwt.ExpiredSignatureError:
            raise UnauthorisedError('Signature expired. Please log in again')
        except jwt.InvalidTokenError:
            raise UnauthorisedError('User unauthorised to make this request')