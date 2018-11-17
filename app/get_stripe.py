import stripe
from stripe import error
from flask import g,current_app


def get_stripe():
    current_app.logger.info(current_app.config['ENV'])
    if 'stripe' not in g:
        if current_app.config['ENV'] == 'test':
            stripe_charge_client = FakeStripe()
        else:
            stripe_client = stripe
            secret_key = current_app.config['STRIPE_SECRET_KEY']
            stripe_client.api_key = secret_key
            stripe_charge_client = stripe_client.Charge
        g.stripe = stripe_charge_client
    return g.stripe

def init_app(app):
    app.app_context()


class FakeStripe:
    def __init__(self):
        self.stripe_calls = None

    def create(self, source, amount, currency, description, fail=False):
        if fail:
            raise error.CardError('This is a fake error')
        else:

            call_params = {'source': source, 'amount': amount,
                           'currency': currency, 'description': description, }
            self.stripe_calls = [1]
            return {'status': 'fake stripe called', **call_params}

    def get_calls(self):
        return self.stripe_calls