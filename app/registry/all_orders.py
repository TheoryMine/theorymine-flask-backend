from app.db import get_db
from flask import current_app

from app.registry.all_actions import AllActions
from app.registry.all_histories import AllHistories
from app.registry.all_points import AllPoints
from app.registry.all_points_history import AllPointsHistory


class AllOrders:
    def __init__(self, logger=None, db=None, all_histories=None, all_actions=None, all_points_history=None,
                 all_points=None):
        self.logger = logger or current_app.logger
        self.db = db or get_db()
        self.all_histories = all_histories or AllHistories()
        self.all_actions = all_actions or AllActions()
        self.all_points_history = all_points_history or AllPointsHistory()
        self.all_points = all_points or AllPoints()

    def add_one(self, user_id, order_name, cursor=None):
        self.logger.info("Adding order")
        transaction = cursor or self.db.cursor()
        history_id = self.all_histories.add_one(cursor=transaction)
        action_id = self.all_actions.add_one(cursor=transaction, user_id=user_id, history_id=history_id)
        point_history_id = self.all_points_history.add_one(cursor=transaction, history_id=history_id,
                                                           action_id=action_id, type = 'order.new.', title = order_name)
        self.all_actions.update_one_obj_id(cursor=transaction, new_obj_id=point_history_id, action_id=action_id)
        theorem_id = self.all_points.copy_one_from_history(cursor=transaction, point_h_id = point_history_id)
        # point_history_id = None
        if cursor is None:
            self.db.commit()
            transaction.close()
        self.logger.info("Done adding order")
        return theorem_id

    def fetch_all_for_user_and_type(self, user_id, type, cursor=None):
        self.logger.info("Fetching orders by user id and type. User id: {},. Type: {}".format(user_id, type))
        transaction = cursor or self.db.cursor()
        query = "SELECT p.id, p.point_type, p.time_stamp, p.title, a.time_stamp as a_time_stamp FROM tm_points as p, tm_actions as a " \
                "WHERE a.user_id = %s AND a.history_id = p.history_id " \
                "AND a.action_type = 'create_point' " \
                "AND point_type LIKE %s " \
                "ORDER BY p.time_stamp DESC, p.id DESC"

        transaction.execute(query, (user_id, type+'%'))
        results = transaction.fetchall()
        if cursor is None:
            transaction.close()
        self.logger.info("Done fetching orders by user id and type. User id: {},. Type: {}".format(user_id, type))
        return results

    def fetch_all_for_user_and_type_with_relations(self, user_id, type, cursor=None):
        self.logger.info("Fetching orders by user id and type. User id: {},. Type: {}".format(user_id, type))
        transaction = cursor or self.db.cursor()
        query = "SELECT p.id, p.point_type, p.time_stamp, p.title," \
                " a.time_stamp AS a_time_stamp, certificate_title " \
                "FROM tm_points AS p " \
                "INNER JOIN tm_actions AS a ON a.history_id = p.history_id " \
                "LEFT JOIN (    " \
                "SELECT src_obj_id, cert.title as certificate_title " \
                "FROM tm_points AS cert " \
                "INNER JOIN tm_relations AS r ON r.dst_obj_id = cert.id " \
                "WHERE cert.point_type = 'certificate.' " \
                "AND r.relation_type = 'has_certificate.' ) AS certRel " \
                "ON  certRel.src_obj_id = p.id " \
                "WHERE a.user_id = %s " \
                "AND a.action_type = 'create_point' " \
                "AND point_type LIKE %s " \
                "ORDER BY p.time_stamp DESC, p.id DESC; "


        print(query)
        transaction.execute(query, (user_id, type+'%'))
        results = transaction.fetchall()
        if cursor is None:
            transaction.close()
        self.logger.info("Done fetching orders by user id and type. User id: {},. Type: {}".format(user_id, type))
        return results


