import stripe
from stripe import error
from flask import g,current_app


def get_stripe():
    current_app.logger.info(current_app.config['ENV'])
    if 'stripe' not in g:
        if current_app.config['ENV'] == 'test':
            stripe_client = FakeStripe()
        else:
            stripe_client = stripe
            secret_key = current_app.config['STRIPE_SECRET_KEY']
            stripe_client.api_key = secret_key
        g.stripe = stripe_client
    return g.stripe

def init_app(app):
    app.app_context()


class FakeStripe:
    def __init__(self):
        self.Charge = Charge()


class Charge:
    def __init__(self):
        self.calls = []

    def create(self, customer, amount, currency, description, fail=False):
        if fail:
            raise error.CardError('This is a fake error')
        else:

            call_params = {'customer': customer, 'amount': amount,
                           'currency': currency, 'description': description, }
            self.calls.append(call_params)
            return {'status': 'fake stripe called', **call_params}

    def get_calls(self):
        return self.calls