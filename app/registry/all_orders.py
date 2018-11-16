from app.db import get_db
from flask import current_app
from app.registry.all_histories import AllHistories


class AllOrders:
    def __init__(self, logger = None , db=None, all_histories = None ):
        self.logger = logger or current_app.logger
        self.db = db or get_db()
        self.all_histories = all_histories or AllHistories()
        self.all_actions = None

    def add_one(self, user_id, order_name, order_body=None, order_status=None, cursor=None):
        self.logger.info("Adding order")
        transaction = cursor or self.db.cursor()
        history_id = self.all_histories.add_one(cursor = transaction)
        # action_id =self.all_actions.add_one(user_id = user_id, history_id= history_id, pid=0, type = 'create_point', body = None)
        # point_history_id = None
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done adding order")
        return {}
