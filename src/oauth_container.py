from dotenv import load_dotenv

from src.core.config import OAuthConfig
from src.utills.oauth import YandexOAuth


load_dotenv('./.environments.stage/.env.auth')

oauth_config = OAuthConfig()
oauth_managers = {
        'yandex': YandexOAuth(client_id=oauth_config.yandex_client_id, client_secret=oauth_config.yandex_client_secret),
    }
