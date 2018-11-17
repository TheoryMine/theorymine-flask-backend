from flask import current_app
from stripe import error

from app.exceptions import StripeCardError
from app.get_stripe import get_stripe


class StripePayments():
    def __init__(self, stripe=None):
        self.logger = current_app.logger
        self.stripe = stripe or get_stripe()

    def charge_customer(self, payment_token, theorem_name):
        try:
            self.logger.info('Charging customer from theorem: ' + theorem_name)
            charge = self.stripe.create(
                source=payment_token,
                amount=1500,
                currency='gbp',
                description=theorem_name
            )
            self.logger.info('Done charging customer from theorem: {}. Charge: {}'.format(theorem_name, charge))
            return charge['status']

        except error.CardError as e:
            raise StripeCardError(e.message)
        except Exception:
            raise StripeCardError('Payment Error')

