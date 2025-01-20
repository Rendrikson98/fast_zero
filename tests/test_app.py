from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_html(client):

    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Hello, World!</h1>' in response.text


def test_create_user(client):

    response = client.post('/users/', json={'username': 'nome do usuário', 'password': 'senha', 'email': 'email@email.com'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'username': 'nome do usuário', 'email': 'email@email.com'}


def test_read_users(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'id': 1, 'username': 'nome do usuário', 'email': 'email@email.com'}]}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/99999',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user(client):
    response = client.get('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'username': 'bob', 'email': 'bob@example.com'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/99999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user_not_found(client):
    response = client.get('/user/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
