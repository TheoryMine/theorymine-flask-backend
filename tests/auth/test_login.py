def test_login_success(client):
    new_user_auth = {
        'email': 'brenda@example.com',
        'password': 'helloBrenda1!'
    }
    client.post('/auth/users', json={ 'first_name': 'Brenda', 'last_name': 'Chan', **new_user_auth })
    api_response = client.post('/auth/session', json=new_user_auth)
    assert api_response.status_code == 200

def test_login_with_non_matching_email_and_password(client):
    new_user_auth = {
        'email': 'brenda@example.com',
        'password': 'helloBrenda1!'
    }
    client.post('/auth/users', json={ 'first_name': 'Brenda', 'last_name': 'Chan', **new_user_auth })
    api_response = client.post('/auth/session', json={ **new_user_auth, 'password':'mammamia@example.com', })
    assert api_response.status_code == 401
