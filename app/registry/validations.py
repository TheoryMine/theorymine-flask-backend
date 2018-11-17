from app.exceptions import BadRequestError

def verify_orders_request_body(json, logger):
    logger.info('Verifying orders body')
    if not json:
        raise BadRequestError('This api call requires a body')
    if 'theorem_name' not in json.keys() or not json['theorem_name'] or not isinstance(json['theorem_name'], str):
        raise BadRequestError('Please provide a theorem name')
    if 'payment_token' not in json.keys() or not json['payment_token']:
        raise BadRequestError('Please provide a payment method')
