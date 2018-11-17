from flask import Blueprint

from app.registry.ordersAPI import OrdersApi

class RegistryResource:

    def __init__(self):
        self.bp = Blueprint('registry', __name__, url_prefix='/registry')
        orders_view = OrdersApi.as_view('orders_api')

        self.bp.add_url_rule(
            '/orders',
            view_func=orders_view,
            methods=['POST', 'GET']
        )
