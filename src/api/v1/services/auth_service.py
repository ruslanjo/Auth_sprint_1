from typing import Any

from src.api.v1.dao.user_dao import UserDAO
from src.db import RedisConnection


class AuthService:
    def __init__(
            self,
            user_dao: UserDAO,
            jwt_config,
            token_generator,
            password_hasher
    ):
        self.user_dao = user_dao
        self.redis = RedisConnection()
        self.jwt_config = jwt_config.dict()
        self.token_generator = token_generator
        self.password_hasher = password_hasher

    def signup(
            self,
            login: str,
            password: str
    ):
        hashed_password = self.password_hasher.hash_password(password)
        return self.user_dao.add_user(
            login,
            hashed_password.decode('utf-8')
        )

    def login(
            self,
            login: str,
            password: str,
            user_agent
    ) -> None | dict:
        user = self.user_dao.get_user(
            login
        )
        if user is None:
            return None
        check_password = self.password_hasher.compare_passwords(password, user.password)
        if not check_password:
            return None

        user_roles = ', '.join(role.name for role in user.roles)
        access_token, refresh_token = self.create_new_jwt_tokens(
            login, user_roles
        )
        self.user_dao.add_login_history(
            user.id,
            user_agent
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def create_new_jwt_tokens(
            self,
            login: str,
            roles: str
    ) -> tuple:
        refresh_token_lifetime = self.jwt_config['refresh_token_lifetime']
        access, refresh = self.token_generator.generate_refresh_and_access_tokens(
            {'login': login,
             'roles': roles}
        )
        self.redis.set_key(
            'refresh_token_' + str(login),
            refresh,
            refresh_token_lifetime,
        )
        return access, refresh

    def get_refresh_token(
            self,
            refresh_token: str
    ) -> tuple[Any, Any] | None:
        result = self.token_generator.check_jwt_token(refresh_token)
        if result.get('result') is False:
            return None

        request_user_login = result.get('data').get('login')
        user_id = self.user_dao.get_user(request_user_login).id
        refresh_on_cache = self.redis.get_key('refresh_token_' + request_user_login)
        if not refresh_on_cache:
            return None

        result['user_id'] = user_id
        if refresh_on_cache.decode('utf-8') == refresh_token:
            return self.create_new_jwt_tokens(
                login=request_user_login, roles=result.get('roles')
            )
        return None

    def logout(
            self,
            access_token: str,
            refresh_token: str
    ) -> None:
        access_token_lifetime = self.jwt_config['access_token_lifetime']
        check_access = self.token_generator.check_jwt_token(access_token)
        check_refresh = self.token_generator.check_jwt_token(refresh_token)

        if not check_access.get('result') and not check_refresh.get('result'):
            return None

        if check_access.get('result'):
            user_login = check_access.get('data').get('login')
            self.redis.set_key(
                'access_token_' + str(user_login),
                access_token,
                access_token_lifetime,
            )
            self.redis.delete_key('refresh_token_' + str(user_login))

        if check_refresh.get('result'):
            user_login = check_refresh.get('data').get('login')
            self.redis.delete_key('refresh_token_' + str(user_login))

    def login_history(
            self,
            login: str
    ) -> list[dict]:
        user_history = self.user_dao.get_login_history(login=login)
        return user_history
