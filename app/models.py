import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Weather(Base):
    """Таблица записей о погоде."""

    id = sa.Column(pg.INTEGER, primary_key=True)
    city = sa.Column(pg.VARCHAR, nullable=False)
    temperature = sa.Column(pg.INTEGER, nullable=False)
    wind_speed = sa.Column(pg.FLOAT)
    humidity = sa.Column(pg.INTEGER)
    created_at = sa.Column(sa.DateTime(), nullable=False, default=func.now())

    __tablename__ = 'weather'

    def __str__(self):
        return (
            f'Запись {self.id} \n\n'
            f'Дата и время: {self.created_at.isoformat(timespec="seconds")} \n'
            f'Город: {self.city} \n'
            f'Температура: {self.temperature} градусов Цельсия \n'
            f'Скорость ветра: {self.wind_speed} м/с \n'
            f'Влажность: {self.humidity}%'
        )
