from validate_email import validate_email
import re
from app.exceptions import BadRequestError

def verify_new_user_request_body(json, logger):
    logger.info('Verifying new user request body')
    if not json:
        raise BadRequestError('This api call requires a body')
    if not all(k in json.keys() for k in ['first_name', 'email', 'password','last_name']):
        raise BadRequestError('first name, last name, email and password should all be provided')
    if not validate_email(json['email']):
            raise BadRequestError('email provided not valid')
    if len(json['password']) < 8:
        raise BadRequestError('Password needs to at lest 8 characters long')
    elif re.search('[0-9]',json['password']) is None:
        raise BadRequestError('Password needs to have at least a number in it')
    elif re.search('[a-zA-Z]',json['password']) is None:
        raise BadRequestError('Password needs to have at least a letter in it')
