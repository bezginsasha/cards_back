from services import auth as auth_service
from utils.constants import AUTH_RESULT

username = 'test_username'
password = 'test_password'


class TestAuth:
    def test_register_service(self):
        register_result = auth_service.register(username, password)
        assert register_result in (AUTH_RESULT['ok'], AUTH_RESULT['username_exists'])

    def test_login_service(self):
        login_result = auth_service.login(username, password)
        assert login_result == AUTH_RESULT['ok']
