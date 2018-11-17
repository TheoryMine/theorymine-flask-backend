import datetime
from app.db import get_db
from flask import current_app

class AllActions:
    def __init__(self, logger = None, db=None,):
        self.logger = logger or current_app.logger
        self.db = db or get_db()

    def add_one(self, user_id, history_id, act_body='', cursor=None):
        self.logger.info("Adding action ")
        transaction = cursor or self.db.cursor()
        insert_query = "INSERT INTO tm_actions " \
                       "(obj_id, action_type, action_body, user_id, ipaddr, time_stamp, history_id) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        transaction.execute(insert_query,
                            (0, 'create_point', act_body, user_id, user_id, datetime.datetime.utcnow(), history_id))
        action_id = transaction.lastrowid
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done adding action: " + str(action_id))
        return action_id

    def update_one_obj_id(self, new_obj_id, action_id, cursor=None):
        self.logger.info("Updating action object id to : {}. Action id: ".format(str(new_obj_id), str(action_id)))
        transaction = cursor or self.db.cursor()
        update_query = "UPDATE tm_actions SET obj_id=%s WHERE id=%s"
        transaction.execute(update_query,
                            (new_obj_id, action_id,))
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info(" Done updating action object id to : {}. Action id: ".format(str(new_obj_id), str(action_id)))
        return
