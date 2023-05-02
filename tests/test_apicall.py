from typing import Any, Dict

import pytest

from app.client import APIClient


def test_api_call_success(
    requests_mock,
    geocoder_resp: Dict[str, Any],
    weather_resp: Dict[str, Any],
    test_api_client: APIClient,
) -> None:
    """Тест успешного вызова АПИ клиента."""
    requests_mock.get(test_api_client.geodecoder_url, json=geocoder_resp)
    requests_mock.get(test_api_client.weather_url, json=weather_resp)
    assert test_api_client('Москва') == weather_resp


def test_api_call_failure(
    requests_mock,
    geocoder_resp: Dict[str, Any],
    weather_resp: Dict[str, Any],
    test_api_client: APIClient,
) -> None:
    """Тест вызова АПИ клиента с несуществующим городом."""
    geocoder_resp['response']['GeoObjectCollection']['featureMember'] = []
    requests_mock.get(test_api_client.geodecoder_url, json=geocoder_resp)
    requests_mock.get(test_api_client.weather_url, json=weather_resp)
    with pytest.raises(ValueError, match='Города ЫЫА не найдено'):
        assert test_api_client('ЫЫА')
