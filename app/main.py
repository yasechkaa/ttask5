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

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.json
        new_task = Task(title=data['title'], content=data.get('content', ''))
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"id": new_task.id, "status": "created"}), 201
    
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "content": t.content} for t in tasks])

@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Not found"}), 404

    if request.method == 'GET':
        cached = cache.get(f"task:{id}")
        if cached:
            return jsonify({"data": json.loads(cached), "source": "redis_cache"})
        task_data = {"id": task.id, "title": task.title, "content": task.content}
        cache.setex(f"task:{id}", 60, json.dumps(task_data))
        return jsonify({"data": task_data, "source": "postgresql_db"})

    if request.method == 'PUT':
        data = request.json
        if 'title' in data: task.title = data['title']
        if 'content' in data: task.content = data['content']
        db.session.commit()
        cache.delete(f"task:{id}")
        return jsonify({"status": "updated"})

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        cache.delete(f"task:{id}")
        return jsonify({"status": "deleted"})