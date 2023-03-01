from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from src.models.user import LoginHistory, User, SocialAccount


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

    def add_user(self, login: str, password: str) -> User:
        new_user = User(
            login=login,
            password=password
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_user(self, login: str) -> [None | tuple[str, str]]:
        return self.session.query(User).filter(User.login == login).first()

    def create_social_account(self, new_user: SocialAccount) -> SocialAccount:
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_user_by_uuid(self, uuid: str) -> None | User:
        return self.session.get(User, uuid)

    def add_login_history(self, user_id: int) -> None:
        login_history = LoginHistory(
            uuid=str(uuid4()),
            user_id=user_id,
            timestamp=datetime.now()
        )
        self.session.add(login_history)
        self.session.commit()

    def get_login_history(self, login: str) -> list[dict]:
        user = self.get_user(login=login)
        history_datetime = [
            str(item.timestamp) for item in self.session.query(LoginHistory).filter(LoginHistory.user_id == user.id)
        ]
        history = [{login: history_datetime}]
        return history

    def update(self, updated_entity: User):
        self.session.add(updated_entity)
        self.session.commit()
        return updated_entity
