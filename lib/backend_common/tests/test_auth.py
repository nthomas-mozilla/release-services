from backend_common.auth import AnonymousUser, TaskclusterUser
from backend_common.mocks import build_header
import pytest
import json


def test_anonymous():
    """
    Test AnonymousUser instances
    """

    user = AnonymousUser()

    # Test base
    assert user.get_id() == 'anonymous:'
    assert user.get_permissions() == set()
    assert user.permissions == set()
    assert not user.is_active
    assert user.is_anonymous


def test_taskcluster_user():
    """
    Test TasklusterUser instances
    """

    credentials = {
        'clientId': 'test/user@mozilla.com',
        'scopes': ['project:test:*', ]
    }
    user = TaskclusterUser(credentials)

    # Test base
    assert user.get_id() == credentials['clientId']
    assert user.get_permissions() == credentials['scopes']
    assert user.permissions == credentials['scopes']
    assert user.is_active
    assert not user.is_anonymous

    # Test invalid input
    with pytest.raises(AssertionError):
        user = TaskclusterUser({})
    with pytest.raises(AssertionError):
        user = TaskclusterUser({'clientId': '', 'scopes': None})


def test_auth(client):
    """
    Test the Taskcluster authentication
    """
    # Test non authenticated endpoint
    resp = client.get('/')
    assert resp.status_code in (200, 302)

    # Test authenticated endpoint without header
    resp = client.get('/test-login')
    assert resp.status_code == 401

    # Test authenticated endpoint with header
    ext_data = {
        'scopes': ['project/test/*', ],
    }
    client_id = 'test/user@mozilla.com'
    header = build_header(client_id, ext_data)
    resp = client.get('/test-login', headers=[('Authorization', header)])
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert data['auth']
    assert data['user'] == client_id
    assert data['scopes'] == ext_data['scopes']


def test_scopes_invalid(client):
    """
    Test the Taskcluster required scopes
    """
    client_id = 'test/user@mozilla.com'

    # Missing a scope to validate test
    ext_data = {
        'scopes': ['project/test/A', 'project/test/C', ],
    }
    header = build_header(client_id, ext_data)
    resp = client.get('/test-scopes', headers=[('Authorization', header)])
    assert resp.status_code == 401


def test_scopes_user(client):
    """
    Test the Taskcluster required scopes
    """
    client_id = 'test/user@mozilla.com'

    # Validate with user scopes
    ext_data = {
        'scopes': ['project/test/A', 'project/test/B', ],
    }
    header = build_header(client_id, ext_data)
    resp = client.get('/test-scopes', headers=[('Authorization', header)])
    assert resp.status_code == 200
    assert resp.data == b'Your scopes are ok.'


def test_scopes_admin(client):
    """
    Test the Taskcluster required scopes
    """
    client_id = 'test/user@mozilla.com'

    # Validate with admin scopes
    ext_data = {
        'scopes': ['project/another/*', 'project/test-admin/*']
    }
    header = build_header(client_id, ext_data)
    resp = client.get('/test-scopes', headers=[('Authorization', header)])
    assert resp.status_code == 200
    assert resp.data == b'Your scopes are ok.'
