from flask import request, jsonify, render_template
from app.projects import projects
from app.projects.models import db, Project, Task
import os
import json
from datetime import datetime

print("Loading projects routes...")  # Debug print statement

@projects.route('/', methods=['POST'])
@projects.route('', methods=['POST'])
def add_project():
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

        name = data.get('name')
        description = data.get('description')
        status = data.get('status')
        due_date_str = data.get('due_date')

        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError as e:
                print(f"Error parsing due_date: {e}")  # Debug print statement
                return jsonify({'error': f"Error parsing due_date: {e}"}), 400
        else:
            due_date = None

        if name:
            project = Project(name=name, description=description, status=status, due_date=due_date)
            db.session.add(project)
            db.session.commit()
            print("Project added to database")  # Debug print statement
            return jsonify({'message': 'Project added successfully!'}), 201
        print("Name is required")  # Debug print statement
        return jsonify({'error': 'Name is required!'}), 400

    print("Request must be JSON")  # Debug print statement
    return jsonify({'error': 'Request must be JSON'}), 400

@projects.route('/', methods=['GET'])
@projects.route('', methods=['GET'])
def get_projects():
    try:
        print("GET request received")  # Debug print statement
        projects = Project.query.all()
        for project in projects:
            project.tasks = Task.query.filter_by(project_id=project.id).all()
        print(f"Projects retrieved: {[project.name for project in projects]}")  # Debug print statement
        return render_template('projects.html', projects=projects)
    except Exception as e:
        print(f"Error retrieving projects: {e}")  # Debug print statement
        return str(e), 500

@projects.route('/api', methods=['GET'])
def get_projects_api():
    try:
        print("API GET request received")  # Debug print statement
        projects = Project.query.all()
        projects_list = [{'id': project.id, 'name': project.name, 'description': project.description, 'status': project.status, 'due_date': project.due_date} for project in projects]
        print(f"Projects retrieved: {projects_list}")  # Debug print statement
        return jsonify(projects_list), 200
    except Exception as e:
        print(f"Error retrieving projects: {e}")  # Debug print statement
        return jsonify({'error': str(e)}), 500

@projects.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    print("DELETE request received")  # Debug print statement
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    print("Project deleted from database")  # Debug print statement
    return jsonify({'message': 'Project deleted successfully!'}), 200
