from flask import Blueprint

from app.auth.loginAPI import LoginAPI
from app.auth.usersAPI import UsersAPI

bp = Blueprint('auth', __name__, url_prefix='/auth')
login_view = LoginAPI.as_view('login_api')
users_view = UsersAPI.as_view('users_api')


bp.add_url_rule(
    '/session',
    view_func=login_view,
    methods=['POST']
)
bp.add_url_rule(
    '/users',
    view_func=users_view,
    methods=['POST']
)