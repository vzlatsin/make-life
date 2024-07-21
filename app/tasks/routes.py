from flask import request, jsonify, render_template
from app.tasks import tasks
from app.projects.models import db, Task

import os
import json

print("Loading tasks routes...")  # Debug print statement



@tasks.route('/', methods=['POST'])
@tasks.route('', methods=['POST'])
def add_task():
    print("POST request received")  # Debug print statement
    print(f"Request Content-Type: {request.content_type}")  # Debug print statement
    print(f"Request data: {request.data}")  # Debug print statement
    print(f"Request form data: {request.form}")  # Debug print statement

    if request.is_json:
        try:
            data = json.loads(request.data.decode('utf-8'))
            print(f"Manually parsed JSON data: {data}")  # Debug print statement
        except Exception as e:
            print(f"Error manually parsing JSON: {e}")  # Debug print statement
            return jsonify({'error': f"Error manually parsing JSON: {e}"}), 400

        content = data.get('content')
        project_id = data.get('project_id')

        if content:
            task = Task(content=content, project_id=project_id)
            db.session.add(task)
            db.session.commit()
            print("Task added to database")  # Debug print statement
            return jsonify({'message': 'Task added successfully!'}), 201
        print("Content is required")  # Debug print statement
        return jsonify({'error': 'Content is required!'}), 400

    print("Request must be JSON")  # Debug print statement
    return jsonify({'error': 'Request must be JSON'}), 400

@tasks.route('/', methods=['GET'])
@tasks.route('', methods=['GET'])
def get_tasks():
    try:
        print("GET request received")  # Debug print statement
        tasks = Task.query.all()
        print(f"Tasks retrieved: {[task.content for task in tasks]}")  # Debug print statement
        return render_template('tasks.html', tasks=tasks)
    except Exception as e:
        print(f"Error retrieving tasks: {e}")  # Debug print statement
        return str(e), 500
    
@tasks.route('/<int:id>', methods=['DELETE'])
def delete_task(id):
    print("DELETE request received")  # Debug print statement
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    print("Task deleted from database")  # Debug print statement
    return jsonify({'message': 'Task deleted successfully!'}), 200
