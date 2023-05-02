from typing import Any, List, Optional

from pydantic import PostgresDsn
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app import models


class DbClient:
    """Клиент Postgres."""

    def __init__(self, uri: PostgresDsn) -> None:
        """Параметры клиента БД.

        Args:
            uri: адрес БД
        """
        self.uri = uri
        self.engine: Optional[Engine] = None
        self.Session: Optional[sessionmaker[Session]] = None

    def connect(self) -> None:
        """Подключение к БД."""
        self.engine = create_engine(self.uri)
        self.Session = sessionmaker(self.engine, expire_on_commit=False, class_=Session)

    def disconnect(self) -> None:
        """Закрытие соединения с БД."""
        self.engine.dispose()

    def add_weather(self, **params: Any) -> None:
        """Добавление записи о погоде.

        Args:
            params: keyword arguments
        """
        with self.Session.begin() as session:
            session.add(models.Weather(**params))
            session.commit()

    def list_weather(self, offset: int) -> List[models.Weather]:
        """Получение списка записей о погоде.

        Args:
            offset: количество записей

        Returns:
            List[models.Weather]: список записей о погоде
        """
        with self.Session.begin() as session:
            order = models.Weather.created_at.desc()
            query = select(models.Weather).order_by(order)
            res = session.execute(query.limit(offset))
            return res.scalars().all()
