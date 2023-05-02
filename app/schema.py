from textwrap import dedent
from typing import List

from pydantic import BaseModel, Field


class GeoResponse(BaseModel):
    """Схема ответа Яндекс.Геокодера.

    Вложенные классы нужны для получения координат.
    """
    class Response(BaseModel):
        """Ответ Яндекс.Геокодера"""

        class _GeoObjectCollection(BaseModel):
            """Коллекция Геообъектов."""

            class GeoObjects(BaseModel):
                """Список полученных Геообъектов."""

                class _GeoObject(BaseModel):
                    """Геообъект."""

                    class GeoPoint(BaseModel):
                        """Координаты Геообъекта"""
                        pos: str

                    Point: GeoPoint

                GeoObject: _GeoObject

            featureMember: List[GeoObjects]

        GeoObjectCollection: _GeoObjectCollection

    response: Response


class Weather(BaseModel):
    """Схема ответа Яндекс.Погоды."""

    class Fact(BaseModel):
        """Текущие показатели погоды."""

        temp: int = Field(..., alias='temperature')
        wind_speed: float
        humidity: int

        class Config:
            """Конфиг."""
            allow_population_by_field_name = True

    fact: Fact

    def __str__(self):
        return (
            f'Текущая температура: {self.fact.temp} градусов Цельсия \n'
            f'Скорость ветра: {self.fact.wind_speed} м/с \n'
            f'Влажность: {self.fact.humidity}%'
        )
