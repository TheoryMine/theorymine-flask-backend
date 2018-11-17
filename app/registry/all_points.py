from app.db import get_db
from flask import current_app


class AllPoints:
    def __init__(self, logger=None, db=None, ):
        self.logger = logger or current_app.logger
        self.db = db or get_db()

    def copy_one_from_history(self, point_h_id, cursor=None):
        self.logger.info("Copying point from point history. Point_h_id: " + str(point_h_id))
        transaction = cursor or self.db.cursor()
        insert_query = "INSERT INTO tm_points" \
                       "(title, body, history_id, action_id, point_type, prev_id, time_stamp) " \
                       "SELECT title, body, history_id, action_id, point_type, id, time_stamp " \
                       "FROM tm_points_history WHERE id = %s"
        transaction.execute(insert_query,
                            (point_h_id, ))
        point_id = transaction.lastrowid
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done copying point from point history. Point_h_id: " + str(point_h_id) +
                         ". Point id: "  + str(point_id))
        return point_id
