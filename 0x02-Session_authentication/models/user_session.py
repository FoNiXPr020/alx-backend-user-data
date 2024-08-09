from models.base import Base
from sqlalchemy import Column, String


class UserSession(Base):
    __tablename__ = 'user_sessions'

    user_id = Column(String(50), nullable=False)
    session_id = Column(String(50), nullable=False, unique=True)

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
