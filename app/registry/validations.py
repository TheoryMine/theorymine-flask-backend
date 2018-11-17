from app.exceptions import BadRequestError

def verify_orders_request_body(json, logger):
    logger.info('Verifying orders body')
    if not json:
        raise BadRequestError('This api call requires a body')
    if not json['theorem_name'] or not isinstance(json['theorem_name'], str):
        raise BadRequestError('theorem name must be provided')
