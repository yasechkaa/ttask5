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

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(200))

# --- Коллекция задач (/tasks) ---

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "content": t.content} for t in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(title=data['title'], content=data.get('content', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "status": "created"}), 201

# --- Конкретная задача (/tasks/<id>) ---

@app.route('/tasks/<int:id>', methods=['GET'])
def get_single_task(id):
    cached = cache.get(f"task:{id}")
    if cached:
        return jsonify({"data": json.loads(cached), "source": "redis_cache"})
    
    task = Task.query.get_or_404(id)
    task_data = {"id": task.id, "title": task.title, "content": task.content}
    cache.setex(f"task:{id}", 60, json.dumps(task_data))
    return jsonify({"data": task_data, "source": "postgresql_db"})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    if 'title' in data: task.title = data['title']
    if 'content' in data: task.content = data['content']
    db.session.commit()
    cache.delete(f"task:{id}")
    return jsonify({"status": "updated"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        cache.delete(f"task:{id}")
    return jsonify({"status": "deleted"})
