import datetime
from app.db import get_db
from flask import current_app

class AllPointsHistory:
    def __init__(self, logger = None, db=None,):
        self.logger = logger or current_app.logger
        self.db = db or get_db()

    def add_one(self, history_id, action_id, title, type, body = None,  cursor=None):
        self.logger.info("Adding point history")
        transaction = cursor or self.db.cursor()
        insert_query = "INSERT INTO tm_points_history" \
                       "(history_id, prev_id, action_id, point_type, title, body, time_stamp) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        transaction.execute(insert_query,
                            (history_id, None, action_id, type, title, body,  datetime.datetime.utcnow()))
        point_history_id = transaction.lastrowid
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done adding point history: " + str(point_history_id))
        return point_history_id
