## Клиент API Яндекс.Погоды

Консольная утилита для получения данных о погоде. Принимает на вход название населенного пункта, выводит в консоль данные о текущей температуре, влажности и направлении ветра в этой географической точке. Сохраняет полученные данные в базу Postgres. 

Использует API Яндекс.Геокодера для получения координат населенного пункта и API Яндекс.Погоды для получения данных о погоде.

Пример использования:

```
Выберите действие 
1 - Новый запрос 
2 - История запросов (1, 2): 1
Введите название города: Москва
Текущая температура: 16 градусов Цельсия 
Скорость ветра: 2.2 м/с 
Влажность: 31%
Сохранить информацию о погоде в базу данных? (да, нет): да
Данные сохранены
```
```
Выберите действие 
1 - Новый запрос 
2 - История запросов (1, 2): 2
Сколько запросов нужно показать? Введите число: 1
Запись 1

Дата и время: 2023-05-02T10:55:48 
Город: Москва 
Температура: 15 градусов Цельсия 
Скорость ветра: 2.0 м/с 
Влажность: 34%
```

### Запуск

В файле `.env` укажите ключи API Яндекс.Геокодера и API Яндекс.Погоды.

Запуск контейнера в интерактивном режиме:
```
$ docker-compose up -d
```
Запуск миграции в БД:
``` 
$ docker-compose exec app bash alembic upgrade head
```
Запуск утилиты:
```
$ docker-compose exec app bash python main.py
```
Запуск тестов:
```
$ docker-compose exec app bash pytest
```