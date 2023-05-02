import json
import os
from typing import Any, Dict, Generator

import pytest
from pydantic import PostgresDsn
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url

from app.client import APIClient
from app.crud import DbClient
from app.models import Base, Weather
from app.settings import Settings


@pytest.fixture
def geocoder_resp() -> Dict[str, Any]:
    """Пример ответа Яндекс.Геокодера."""
    file = open('tests/fixtures/geocoder.json')
    return json.load(file)


@pytest.fixture
def weather_resp():
    """Пример ответа Яндекс.Погоды."""
    file = open('tests/fixtures/weather.json')
    return json.load(file)


@pytest.fixture(scope='session')
def conf() -> Settings:
    """Тестовые настройки."""
    os.environ['POSTGRES_DB'] = 'pytest'
    settings = Settings()
    assert settings
    return settings


@pytest.fixture
def test_api_client(conf: Settings) -> APIClient:
    """Тестовый АПИ клиент."""
    return APIClient(conf)


@pytest.fixture(scope='session')
def database(conf: Settings) -> Generator:
    """Тестовая БД."""
    assert conf.POSTGRES_DB == 'pytest'
    assert conf.POSTGRES_URI
    create_database(conf.POSTGRES_URI)
    engine = create_engine(conf.POSTGRES_URI)
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        engine.dispose()
        drop_database(conf.POSTGRES_URI)


@pytest.fixture
def test_db_client(conf: Settings, database: Engine) -> Generator:
    """Клиент тестовой БД."""
    client = DbClient(conf.POSTGRES_URI)
    client.connect()
    try:
        yield client
    finally:
        client.disconnect()


@pytest.fixture
def record(test_db_client: DbClient) -> Weather:
    """Запись о погоде."""
    item = Weather(city='Москва', temperature=11, wind_speed=3.7, humidity=49)
    with test_db_client.Session() as session:
        session.add(item)
        session.commit()
        session.flush()
    return item


def create_database(url: PostgresDsn) -> None:
    """Создание тестовой БД."""
    url_obj = make_url(url)
    nodb_url = url_obj.set(database='')
    engine = create_engine(nodb_url, isolation_level='AUTOCOMMIT')
    conn = engine.connect()
    conn.execute(text('CREATE DATABASE pytest'))
    conn.close()


def drop_database(url: PostgresDsn) -> None:
    """Удаление тестовой БД."""
    url_obj = make_url(url)
    nodb_url = url_obj.set(database='')
    engine = create_engine(nodb_url, isolation_level='AUTOCOMMIT')
    conn = engine.connect()
    conn.execute(text('DROP DATABASE pytest'))
    conn.close()
