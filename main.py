import sys
from typing import Tuple

import click

from app.client import APIClient
from app.crud import DbClient
from app.schema import Weather
from app.settings import Settings


def init() -> Tuple[APIClient, DbClient]:
    """Инициализация АПИ клиента и БД клиента."""
    conf = Settings()
    api_client = APIClient(conf)
    db_client = DbClient(conf.POSTGRES_URI)
    db_client.connect()
    return api_client, db_client


def choose_action() -> str:
    """Ввод пользователя выбор действия."""
    return click.prompt(
        'Выберите действие \n1 - Новый запрос \n2 - История запросов',
        type=click.Choice(['1', '2']),
    )


def choose_city() -> str:
    """Ввод пользователя название города."""
    return click.prompt('Введите название города')


def save_or_no() -> str:
    """Ввод пользователя сохранить/не сохранить запись."""
    return click.prompt(
        'Сохранить информацию о погоде в базу данных?',
        type=click.Choice(['да', 'нет']),
    )


def choose_offset() -> int:
    """Ввод пользователя количество последних записей."""
    return int(click.prompt('Сколько запросов нужно показать? Введите число'))


@click.command()
def run() -> None:
    """Запуск CLI."""
    api_client, db_client = init()
    try:
        action = choose_action()
        if action == '1':
            city = choose_city()
            resp = api_client(city)
            weather = Weather(**resp)
            click.echo(weather)
            save = save_or_no()
            if save == 'да':
                db_client.add_weather(city=city, **weather.fact.dict(by_alias=True))
                click.echo('Данные сохранены')
        elif action == '2':
            offset = choose_offset()
            records = db_client.list_weather(offset)
            for record in records:
                click.echo(record)
    except ValueError as err:
        click.echo(err)
    except click.Abort:
        click.echo('Aborted!')
        sys.exit(1)


if __name__ == '__main__':
    run()
