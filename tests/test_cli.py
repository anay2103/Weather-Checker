import json
from typing import Any, Dict

import pytest

from click.testing import CliRunner

import main
from app import crud, schema, models


class FakeClient:
    """Поддельный API клиент."""

    def __call__(self, city: str) -> Dict[str, Any]:
        file = open('tests/fixtures/weather.json')
        return json.load(file)


@pytest.fixture
def fake_client() -> FakeClient:
    """Объект поддельного API клиента."""
    return FakeClient()


def test_cli_run_1(
    monkeypatch: pytest.MonkeyPatch,
    fake_client: FakeClient,
    test_db_client: crud.DbClient
) -> None:
    """Тест стандартного вывода CLI. Новый запрос к API погоды."""
    monkeypatch.setattr('main.init', lambda: (fake_client, test_db_client))
    monkeypatch.setattr('main.choose_action', lambda: '1')
    monkeypatch.setattr('main.choose_city', lambda: 'Москва')
    monkeypatch.setattr('main.save_or_no', lambda: 'нет')

    call = fake_client('Москва')
    output = str(schema.Weather(**call))
    runner = CliRunner()
    result = runner.invoke(main.run)
    assert result.output == f'{output}\n'
    assert result.exit_code == 0


def test_cli_run_2(
    monkeypatch: pytest.MonkeyPatch,
    fake_client: FakeClient,
    test_db_client: crud.DbClient,
    record: models.Weather,
) -> None:
    """Тест стандартного вывода CLI. Запрос записей в БД."""
    monkeypatch.setattr('main.init', lambda: (fake_client, test_db_client))
    monkeypatch.setattr('main.choose_action', lambda: '2')
    monkeypatch.setattr('main.choose_offset', lambda: '2')

    output = str(record)
    runner = CliRunner()
    result = runner.invoke(main.run)
    assert result.output == f'{output}\n'
    assert result.exit_code == 0
