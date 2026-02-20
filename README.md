проверка 😭🙏🏻🍕🥹💋💪🏻 
`curl -X POST http://localhost/tasks -H "Content-Type: application/json" -d '{"name": "aosoos", "email": "admin@example.com"}'`
создать новую задачу

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

