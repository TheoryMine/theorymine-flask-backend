import uuid
import time

def register_new_user(client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda+{}@example.com'.format(str(uuid.uuid4())),
        'password': 'helloBrenda1!'
    }
    registration_response = client.post('/auth/users', json=new_user)
    registered_user = registration_response.json
    return registered_user

def get_unique_key_from_db(db):
    transaction = db.cursor()
    select_query = "SELECT id FROM tm_unique_keys "
    transaction.execute(select_query)
    results = transaction.fetchone()
    return results

def get_actions_for_history_from_db(db, history_id):
    transaction = db.cursor()
    select_query = "SELECT * FROM tm_actions WHERE history_id = %s "
    transaction.execute(select_query, (history_id,))
    results = transaction.fetchall()
    return results

def get_point_hist_for_history_from_db(db, history_id):
    transaction = db.cursor()
    select_query = "SELECT * FROM tm_points_history WHERE history_id = %s "
    transaction.execute(select_query, (history_id,))
    results = transaction.fetchall()
    return results

def get_point_from_db(db, point_id):
    transaction = db.cursor()
    select_query = "SELECT * FROM tm_points WHERE id = %s "
    transaction.execute(select_query, (point_id,))
    results = transaction.fetchall()
    return results

################### POST
def test_post_to_orders_success(stripe, db, client):
    user = register_new_user(client)
    auth_token = user['auth_token']
    user_id = user['user_id']

    new_order = {
        'theorem_name': 'Brenda Theorem',
    }
    payment_token ='123'
    api_response = client.post('/registry/orders',
                               json={'payment_token': payment_token, **new_order},
                               headers={'Authorization': 'Bearer ' + auth_token})

    assert api_response.status_code == 201
    assert api_response.content_type == 'application/json'
    theorem_id = api_response.json['theorem_id']
    assert theorem_id is not None

    history = get_unique_key_from_db(db)
    history_id = history['id']
    assert history_id is not None

    point_h = get_point_hist_for_history_from_db(db, history_id)
    point_h_id = point_h[0]['id']
    assert point_h_id is not None

    action = get_actions_for_history_from_db(db, history_id)
    action_id = action[0]['id']
    assert action_id is not None

    point = get_point_from_db(db, theorem_id)


    assert len(point_h) == 1
    assert (point_h[0]['action_id']) == action_id
    assert (point_h[0]['point_type']) == 'order.new.'
    assert (point_h[0]['title']) == new_order['theorem_name']

    assert len(point) == 1
    assert (point[0]['point_type']) == 'order.new.'
    assert (point[0]['title']) == new_order['theorem_name']
    assert (point[0]['history_id']) == history_id
    assert (point[0]['action_id']) == action_id
    assert (point[0]['prev_id']) == point_h_id

    assert len(action) == 1
    assert (action[0]['user_id']) == user_id
    assert (action[0]['history_id']) == history_id
    assert (action[0]['action_type']) == 'create_point'
    assert (action[0]['obj_id']) == point_h_id


def test_post_unauthorised_with_no_token(client):
    body = {'theorem_name': 'Brenda Theorem','payment_token': '123'}
    api_response = client.post('/registry/orders', json=body)
    assert api_response.status_code == 401


def test_post_unauthorised_with_expired_token(client):
    user = register_new_user(client)
    auth_token = user['auth_token']

    time.sleep(1)

    body = {'theorem_name': 'Brenda Theorem','payment_token': '123'}
    api_response = client.post('/registry/orders',
                               json=body,
                               headers={'Authorization': 'Bearer ' + auth_token})
    assert api_response.status_code == 401


def test_post_to_orders_missing_theorem_name(client):
    user = register_new_user(client)
    auth_token = user['auth_token']

    body = {'theorem_name': None,'payment_token': '123'}

    api_response = client.post('/registry/orders',
                               json=body,
                               headers={'Authorization': 'Bearer ' + auth_token})

    assert api_response.status_code == 400


def test_post_to_orders_missing_payment_token(client):
    user = register_new_user(client)
    auth_token = user['auth_token']

    body = {'theorem_name': 'blah' }

    api_response = client.post('/registry/orders',
                               json=body,
                               headers={'Authorization': 'Bearer ' + auth_token})

    assert api_response.status_code == 400

############## GET


def test_get_to_orders_success(db, client):
    user = register_new_user(client)
    auth_token = user['auth_token']
    user_id = user['user_id']

    new_order1 = {'theorem_name': 'Brenda Theorem',}
    new_order2 = {'theorem_name': 'Patato Theorem',}
    payment_token ='123'
    client.post('/registry/orders',json={'payment_token': payment_token, **new_order1},headers={'Authorization': 'Bearer ' + auth_token})
    client.post('/registry/orders',json={'payment_token': payment_token, **new_order2},headers={'Authorization': 'Bearer ' + auth_token})

    api_response = client.get('/registry/orders', headers={'Authorization': 'Bearer ' + auth_token})
    assert api_response.status_code == 200

def test_get_unauthorised_with_no_token(client):
    api_response = client.get('/registry/orders')
    assert api_response.status_code == 401


def test_get_unauthorised_with_expired_token(client):
    user = register_new_user(client)
    auth_token = user['auth_token']

    time.sleep(1)
    api_response = client.get('/registry/orders',
                               headers={'Authorization': 'Bearer ' + auth_token})
    assert api_response.status_code == 401

