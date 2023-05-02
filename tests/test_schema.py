from typing import Any, Dict

from app import schema


def test_geocoder_schema(geocoder_resp: Dict[str, Any]) -> None:
    """Тест схемы ответа API Яндекс.Геокодера."""
    georesponse = schema.GeoResponse(**geocoder_resp)
    assert georesponse
    assert georesponse.response
    assert georesponse.response.GeoObjectCollection
    assert georesponse.response.GeoObjectCollection.featureMember[0]
    assert georesponse.response.GeoObjectCollection.featureMember[0].GeoObject
    assert georesponse.response.GeoObjectCollection.featureMember[0].GeoObject.Point.pos


def test_weather_schema(weather_resp: Dict[str, Any]) -> None:
    """Тест схемы ответа API Яндекс.Погоды."""
    weather = schema.Weather(**weather_resp)
    assert weather
    assert weather.fact
    assert weather.fact.temp
    assert weather.fact.humidity
    assert weather.fact.wind_speed
