from flask import Blueprint

from app.registry.ordersAPI import OrdersApi

bp = Blueprint('registry', __name__, url_prefix='/registry')
orders_view = OrdersApi.as_view('orders_api')


bp.add_url_rule(
    '/orders',
    view_func=orders_view,
    methods=['POST']
)
