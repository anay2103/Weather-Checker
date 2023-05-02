from typing import Any, Dict

import requests

from app.schema import GeoResponse
from app.settings import Settings


class APIClient:

    def __init__(self, settings: Settings) -> None:
        """Параметры АПИ клиента.

        Args:
            settings: настройки проекта
        """
        self.geodecoder_url = 'https://geocode-maps.yandex.ru/1.x/?format=json&results=1'
        self.weather_url = 'https://api.weather.yandex.ru/v2/forecast?limit=1&hours=false'
        self.settings = settings

    def __call__(self, city: str) -> Dict[str, Any]:
        """Запросы к API Яндекс.Геокодера и Яндекс.Погоды для получения сведений о погоде.

        Args:
            city: название города, погоду в котором нужно запросить

        Returns:
            Dict[str, Any]: десериализованный ответ АПИ

        """
        geocod_payload = {'apikey': self.settings.GEOCODER_KEY, 'geocode': city}
        try:
            geocod_resp = requests.get(self.geodecoder_url, params=geocod_payload)
        except UnicodeEncodeError:
            raise ValueError(f'Города {city} не найдено')
        geocod_resp.raise_for_status()
        geo = GeoResponse(**geocod_resp.json())
        try:
            lon, lat = geo.response.GeoObjectCollection.featureMember[0].GeoObject.Point.pos.split()
        except IndexError:
            raise ValueError(f'Города {city} не найдено')

        weather_payload = {'lon': lon, 'lat': lat}
        weather_headers = {'X-Yandex-API-Key': self.settings.WEATHER_KEY}
        weather_resp = requests.get(self.weather_url, headers=weather_headers, params=weather_payload)
        weather_resp.raise_for_status()
        return weather_resp.json()
