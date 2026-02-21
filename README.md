# Структура и наполнение базы (PostgreSQL)
## Схема таблицы task
База данных создается автоматически при запуске приложения.
| Поле | Тип | Описание |
| :--- | :--- | :--- |
| **id** | Integer | Уникальный ключ (PK) |
| **title** | String | Заголовок (Обязательно) |
| **content** | String | Описание (Опционально) |

Чтобы добавить данные в пустую базу, используй команду curl в терминале:
`curl -X POST http://localhost/tasks -H "Content-Type: application/json" -d '{"name": "aosoos", "content": "admin@example.com"}'`

## Если нужно зайти в саму базу через Docker и посмотреть записи:
1. Зайти в базу
docker exec -it task5_db_1 psql -U user -d crud_db

2. Посмотреть таблицу
SELECT * FROM task;

# Команды для проверки работы: 
`curl http://localhost/tasks`
получить список задач

`curl -X PUT http://localhost/tasks/1 -H "Content-Type: application/json" -d '{"email": "new@example.com"}'`
обновить задачу с id 1

`curl -X DELETE http://localhost/tasks/1`
удалить задачу с id 1

`docker exec -it dz5-db-1 psql -U user -d flask_db`
зайти в базу данных

`\dt`
показать список таблиц

`\d task`
показать структуру таблицы task

`select * from task`
показать все записи в таблице task

`docker compose logs -f nginx`
смотреть логи nginx

`docker compose logs -f db`
смотреть логи базы данных

`docker compose logs -f web`
смотреть логи web-сервиса

