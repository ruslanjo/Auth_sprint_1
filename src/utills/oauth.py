import abc
import http
import json
import urllib.parse

import requests

from src.container import oauth_config


class OAuthManager(abc.ABC):
    @property
    @abc.abstractmethod
    def user_id_api_field(self):
        '''
        Аттрибут используется в Service слое, чтобы динамически получать по ключу уникальный id
        пользователя в сервисе провайдере
        Аттрибут - это название поля, содержащего id пользователя в провайдере
        '''
        pass

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @abc.abstractmethod
    def get_tokens(self, verification_code: str):
        pass

    @abc.abstractmethod
    def exchange_token_on_data(self, access_token: str):
        pass

    @abc.abstractmethod
    def activate_refresh_token(self, refresh_token: str):
        pass


class YandexOAuth(OAuthManager):
    user_id_api_field = 'id'

    def _prepare_token_request_body(self,
                                    verification_code: str = None,
                                    grant_type: str = 'authorization_code',
                                    refresh_token: str = None,
                                    scope: str = None) -> str:
        """
        :param verification_code: Authorization code, который возвращается из Yandex Auth в callback uri
        :param grant_type: Параметр опеределяет тип запроса к токену
        :param refresh_token: Передаётся если grant_type = refresh_token
        :param scope: ресурсы, к которым запрашивается доступ
        :return: x-www-form-urlencoded строку, которая передаётся в body POST запроса
        """
        query = {
            'grant_type': grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        if grant_type == 'authorization_code':
            query['code'] = verification_code
        if grant_type == 'refresh_token':
            query['refresh_token'] = refresh_token
        if scope:
            query['scope'] = scope

        return urllib.parse.urlencode(query)  # converting to x-www-form-urlencoded

    def get_tokens(self,
                   verification_code: str,
                   grant_type: str = 'authorization_code',
                   scope: str = 'openid login:email login:info') -> dict[str: str] | None:
        """
        Обмен Authorization_code на токены
        https://yandex.ru/dev/id/doc/ru/codes/code-url
        """

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        query = self._prepare_token_request_body(verification_code, grant_type, scope)

        response = requests.post(url=oauth_config.yandex_token_uri, headers=headers, data=query)
        try:
            response = response.json()
        except json.JSONDecodeError:
            return None
        if response.get('error'):
            return None
        return response

    def exchange_token_on_data(self, access_token: str) -> dict | None:
        headers = {'Authorization': f'OAuth {access_token}'}

        user_data = requests.post(url=oauth_config.yandex_resource_server,
                                  headers={headers}
                                  )
        if user_data.status_code == http.HTTPStatus.UNAUTHORIZED:
            return None
        try:
            return user_data.json()
        except json.JSONDecodeError:
            return None

    def activate_refresh_token(self, refresh_token: str) -> None | tuple[str, str]:
        query = self._prepare_token_request_body(grant_type='refresh_token',
                                                 refresh_token=refresh_token
                                                 )
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url=oauth_config.yandex_token_uri,
                                 headers=headers,
                                 data=query)
        try:
            data = response.json()
        except json.JSONDecodeError:
            return None
        if data.get('error'):
            return None
        return data.get('access_token'), data.get('refresh_token')
