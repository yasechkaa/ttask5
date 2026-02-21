# Структура и наполнение базы (PostgreSQL)
Схема таблицы users 
| Поле | Тип | Описание |
| :--- | :--- | :--- |
| **id** | Integer | Уникальный ключ (Primary Key) |
| **name** | String | Имя пользователя (Обязательно) |
| **surname** | String | Фамилия (Обязательно) |
| **age** | Integer | Возраст (18-100) |
| **town** | String | Город проживания |

## Команды для управления и проверки

curl http://localhost/users — получить список всех пользователей.

curl http://localhost/users/1 — получить данные пользователя с ID 1 (проверка кэша Redis).

curl -X POST http://localhost/users -H "Content-Type: application/json" -d '{"name": "aosoos", "surname": "admin", "age": 20, "town": "Moscow"}' — добавить нового пользователя.

curl -X PUT http://localhost/users/1 -H "Content-Type: application/json" -d '{"age": 25}' — обновить данные пользователя.

curl -X DELETE http://localhost/users/1 — удалить пользователя.

## Работа с базой данных внутри Docker:

sudo docker exec -it task5_db_1 psql -U user -d crud_db — зайти в консоль PostgreSQL.

\dt — показать список таблиц (должна быть users).

\d users — показать структуру таблицы пользователей.

SELECT * FROM users; — показать все записи в таблице.

## Просмотр логов (если что-то не работает):

sudo docker-compose logs -f app — логи Python-приложения (Flask + Gunicorn).

sudo docker-compose logs -f db — логи базы данных.

sudo docker-compose logs -f redis — логи кэш-сервера.
