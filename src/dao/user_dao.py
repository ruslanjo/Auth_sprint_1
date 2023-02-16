from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from src.models.user import User, LoginHistory


class BaseUser(ABC):
    @abstractmethod
    def add_user(self, login: str, password: str) -> None:
        pass

    @abstractmethod
    def get_user(self, login: str) -> [None | tuple[str, str]]:
        pass


class UserDAO(BaseUser):
    def __init__(self, session):
        self.session = session

    def add_user(self, login: str, password: str) -> None:
        new_user = User(
            login=login,
            password=password
        )
        self.session.add(new_user)
        self.session.commit()

    def get_user(self, login: str) -> [None | tuple[str, str]]:
        return self.session.query(User).filter(User.login == login).first()

    def add_login_history(self, user_id: int) -> None:
        login_history = LoginHistory(
            uuid=str(uuid4()),
            user_id=user_id,
            timestamp=datetime.now()
        )
        self.session.add(login_history)
        self.session.commit()
