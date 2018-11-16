import hashlib
from app.db import get_db
from app.exceptions import BadRequestError

class AllUsers:
    def __init__(self, logger):
        self.logger = logger
        self.db = get_db()

    def add_one(self, last_name, first_name, email, password, userkind='normal', cursor=None):
        self.logger.info("Adding user")
        transaction = cursor or self.db.cursor()
        existing_user = self.fetch_one_by_email(email, cursor)
        if existing_user:
            raise BadRequestError('User with this email already registered')
        password_to_encode = '{0}.{1}'.format(email, password)
        password = hashlib.md5(password_to_encode.encode()).hexdigest()
        insert_query = "INSERT INTO tm_users(lastname, firstname, email, password, last_act_kind, userkind) " \
                       "VALUES (%s, %s, %s, %s, %s, %s)"
        transaction.execute(insert_query, (last_name, first_name, email, password, 'new_user', userkind))
        new_user = self.fetch_one_by_email(email, cursor)
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done adding user")
        return {'user_id': new_user['id']}

    def fetch_one_by_email(self, email, cursor=None):
        self.logger.info("Fetching user by email")
        transaction = cursor or self.db.cursor()
        query = "SELECT id, lastname, firstname, email, password, userkind, last_act_kind, last_act_time, last_act_code " \
                "FROM tm_users WHERE email = %s;"
        transaction.execute(query, (email,))
        results = transaction.fetchone()
        if cursor is None:
            transaction.close()
        self.logger.info("Done fetching user by email")
        return results

    def fetch_one_by_email_and_password(self, email, password, cursor=None):
        self.logger.info("Fetching user by email and password")
        transaction = cursor or self.db.cursor()
        password_to_encode = '{0}.{1}'.format(email, password)

        password = hashlib.md5(password_to_encode.encode()).hexdigest()
        query = "SELECT id FROM tm_users WHERE email = %s AND password = %s ;"
        transaction.execute(query, (email,password))
        results = transaction.fetchone()
        if cursor is None:
            transaction.close()
        self.logger.info("Done fetching user by email and password")
        return results
