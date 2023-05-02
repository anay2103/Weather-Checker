from app.crud import DbClient


def test_add_weather_record(test_db_client: DbClient) -> None:
    """Тест добавления записи о погоде."""
    test_db_client.add_weather(
        city='Простоквашино',
        temperature=10,
        wind_speed=10,
        humidity=10,
    )


def test_list_weather_records(test_db_client: DbClient) -> None:
    """Тест просмотра записей о погоде."""
    res = test_db_client.list_weather(offset=1)

    assert res
    assert len(res) == 1
    assert res[0].city == 'Простоквашино'
    assert res[0].temperature == 10
    assert res[0].wind_speed == 10
    assert res[0].humidity == 10
