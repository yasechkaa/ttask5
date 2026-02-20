curl -X POST http://localhost/tasks -H "Content-Type: application/json" -d '{"name": "aosoos", "email": "admin@example.com"}'

curl http://localhost/tasks

curl -X PUT http://localhost/tasks/1 -H "Content-Type: application/json" -d '{"email": "new@example.com"}'

curl -X DELETE http://localhost/tasks/1

docker exec -it dz5-db-1 psql -U user -d flask_db

\dt

\d "user"

docker compose logs -f nginx

docker compose logs -f db

docker compose logs -f web
