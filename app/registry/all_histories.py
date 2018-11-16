from app.db import get_db
from flask import current_app

class AllHistories:
    def __init__(self, logger = None, db=None,):
        self.logger = logger or current_app.logger
        self.db = db or get_db()

    def add_one(self, cursor=None):
        self.logger.info("Adding history id")
        transaction = cursor or self.db.cursor()
        insert_query = "INSERT INTO tm_unique_keys () VALUES ()"
        transaction.execute(insert_query)
        history_id = transaction.lastrowid
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done adding history id: "+ str(history_id))
        return history_id
