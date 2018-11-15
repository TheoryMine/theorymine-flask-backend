import hashlib

def get_user_from_db(db, user_id):
    transaction = db.cursor()
    select_query = "SELECT id, firstname, lastname, email, password, userkind  FROM tm_users WHERE id = %s "
    transaction.execute(select_query, (user_id,))
    results = transaction.fetchall()
    return results

def test_post_to_users_success(db, client):
    new_user = {
        'first_name': 'Brenda',
        'last_name': 'Chan',
        'email': 'brenda@example.com',
        'password': 'helloBrenda!'

    }
    api_response = client.post('/users/users', json=new_user)
    assert api_response.status_code == 201
    user_id = api_response.json['user_id']
    assert user_id is not None
    user_values = get_user_from_db(db, user_id)
    assert len(user_values) == 1

    assert user_values[0]['firstname'] == new_user['first_name']
    assert user_values[0]['lastname'] == new_user['last_name']
    assert user_values[0]['email'] == new_user['email']
    assert user_values[0]['password'] == hashlib.md5(b'brenda@example.com.helloBrenda!').hexdigest()

