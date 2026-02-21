from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cache = redis.Redis(host='redis', port=6379, db=0)

# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    town = db.Column(db.String(100), nullable=False)

# 1. Получить всех пользователей (напрямую из БД)
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "surname": u.surname, "age": u.age, "town": u.town} for u in users])

# 2. Получить одного пользователя (с использованием Redis)
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    cached = cache.get(f"user:{id}")
    if cached:
        return jsonify({"data": json.loads(cached), "source": "redis_cache"})

    user = User.query.get_or_404(id)
    user_data = {"id": user.id, "name": user.name, "surname": user.surname, "age": user.age, "town": user.town}
    
    # Кэшируем на 60 секунд
    cache.setex(f"user:{id}", 60, json.dumps(user_data))
    return jsonify({"data": user_data, "source": "postgresql"})

# 3. Создать нового пользователя (POST)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not all(k in data for k in ("name", "surname", "age", "town")):
        return jsonify({"error": "Missing fields (name, surname, age, town)"}), 400

    new_user = User(
        name=data['name'],
        surname=data['surname'],
        age=data['age'],
        town=data['town']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "created", "id": new_user.id}), 201

# 4. Обновить данные (Инвалидация кэша)
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    
    if 'name' in data: user.name = data['name']
    if 'surname' in data: user.surname = data['surname']
    if 'age' in data: user.age = data['age']
    if 'town' in data: user.town = data['town']
    
    db.session.commit()
    cache.delete(f"user:{id}") # Удаляем старый кэш
    return jsonify({"status": "updated"})

# 5. Удалить пользователя (Удаление из БД и кэша)
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    cache.delete(f"user:{id}")
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
