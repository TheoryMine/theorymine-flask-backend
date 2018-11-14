from  MySQLdb import connect, cursors
from flask import g, current_app


def get_db():
    if 'db' not in g:
        mysql_db = connect(host= current_app.config['DATABASE_HOST'],
                          user=current_app.config['DATABASE_USER'],
                          passwd=current_app.config['DATABASE_PASSWORD'],
                          db=current_app.config['DATABASE_NAME'],
                          cursorclass=cursors.DictCursor)
        g.db = mysql_db
    return g.db

def truncate_db():
    db = get_db()
    cursor= db.cursor()
    queries = [
        "DELETE FROM tm_actions",
        "DELETE FROM tm_paypal_payment_info",
        "DELETE FROM tm_points",
        "DELETE FROM tm_points_history",
        "DELETE FROM tm_relations",
        "DELETE FROM tm_relations_history",
        "DELETE FROM tm_unique_keys",
        "DELETE FROM tm_users",
    ]
    [cursor.execute(query) for query in queries]


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
