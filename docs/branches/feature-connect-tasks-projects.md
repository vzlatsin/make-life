Here's the document template for the branch focused on connecting tasks to projects:

### Document for `feature/connect-tasks-projects`

#### `docs/branches/feature-connect-tasks-projects.md`

```markdown
# Connect Tasks to Projects Documentation

## Branch: `feature/connect-tasks-projects`

### Purpose

The purpose of this branch is to connect tasks to projects, ensuring each task can be associated with a specific project. This includes updating the database schema, backend logic, and user interface to accommodate this relationship.

### Steps Taken

1. **Create and Switch to a New Branch**
   - We create a new branch for connecting tasks to projects to keep changes organized.
   ```bash
   git checkout -b feature/connect-tasks-projects
   ```

2. **Update Database Models**
   - Modify the `Task` model to include a foreign key reference to the `Project` model.

   #### `app/tasks/models.py`
   ```python
   from app import db

   class Task(db.Model):
       __tablename__ = 'tasks'
       id = db.Column(db.Integer, primary_key=True)
       content = db.Column(db.Text, nullable=False)
       project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
       project = db.relationship('Project', back_populates='tasks')

   class Project(db.Model):
       __tablename__ = 'projects'
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100), nullable=False)
       description = db.Column(db.Text, nullable=True)
       tasks = db.relationship('Task', back_populates='project')
   ```

3. **Create and Apply Database Migrations**
   - Generate and apply migrations to update the database schema with the new relationship.

   ```bash
   flask db migrate -m "Add project_id to tasks"
   flask db upgrade
   ```

4. **Update Routes**
   - Update the task routes to handle the association with projects.

   #### `app/tasks/routes.py`
   ```python
   from flask import request, jsonify, render_template
   from app.tasks import tasks
   from app.tasks.models import db, Task
   from app.projects.models import Project

   @tasks.route('/', methods=['POST'])
   def add_task():
       if request.is_json:
           data = request.get_json()
       else:
           data = request.form

       content = data.get('content')
       project_id = data.get('project_id')

       if content and project_id:
           project = Project.query.get(project_id)
           if not project:
               return jsonify({'error': 'Invalid project ID'}), 400

           task = Task(content=content, project_id=project_id)
           db.session.add(task)
           db.session.commit()
           return jsonify({'message': 'Task added successfully!'}), 201

       return jsonify({'error': 'Content and project_id are required!'}), 400

   @tasks.route('/', methods=['GET'])
   def get_tasks():
       tasks = Task.query.all()
       return render_template('tasks.html', tasks=tasks)

   @tasks.route('/<int:id>', methods=['DELETE'])
   def delete_task(id):
       task = Task.query.get_or_404(id)
       db.session.delete(task)
       db.session.commit()
       return jsonify({'message': 'Task deleted successfully!'}), 200
   ```

5. **Update User Interface**
   - Modify the task form to include a dropdown for selecting a project.

   #### `app/tasks/templates/tasks.html`
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Tasks</title>
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
       <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
       <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
       <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
   </head>
   <body>
       <div class="sidebar">
           <h4 class="text-center">Make-Life App</h4>
           <a href="/capture"><i class="fas fa-pencil-alt"></i> Capture</a>
           <a href="/projects"><i class="fas fa-project-diagram"></i> Projects</a>
           <a href="/tasks"><i class="fas fa-tasks"></i> Tasks</a>
       </div>
       <div class="content">
           <h1>Tasks</h1>
           <form id="taskForm" class="form-inline my-2 my-lg-0">
               <input class="form-control mr-sm-2" type="text" id="taskInput" placeholder="Add a task" required>
               <select class="form-control" id="projectSelect">
                   {% for project in projects %}
                       <option value="{{ project.id }}">{{ project.name }}</option>
                   {% endfor %}
               </select>
               <button class="btn btn-outline-success my-2 my-sm-0" type="submit"><i class="fas fa-plus"></i> Add</button>
           </form>
           <ul class="list-group mt-3" id="taskList">
               {% for task in tasks %}
                   <li class="list-group-item">
                       {{ task.content }} (Project: {{ task.project.name }})
                       <button class="btn btn-danger btn-sm" onclick="deleteTask({{ task.id }})"><i class="fas fa-trash-alt"></i></button>
                   </li>
               {% endfor %}
           </ul>
       </div>
       <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js"></script>
       <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>
       <script>
           document.getElementById('taskForm').addEventListener('submit', function(event) {
               event.preventDefault();
               const content = document.getElementById('taskInput').value;
               const projectId = document.getElementById('projectSelect').value;
               fetch('/tasks/', {
                   method: 'POST',
                   headers: {
                       'Content-Type': 'application/json',
                   },
                   body: JSON.stringify({ content: content, project_id: projectId }),
               }).then(response => response.json())
               .then(data => {
                   if (data.message) {
                       location.reload();
                   } else {
                       alert(data.error || 'An error occurred');
                   }
               });
           });

           function deleteTask(id) {
               fetch(`/tasks/${id}`, {
                   method: 'DELETE',
               }).then(response => response.json())
               .then(data => {
                   if (data.message) {
                       location.reload();
                   } else {
                       alert(data.error || 'An error occurred');
                   }
               });
           }
       </script>
   </body>
   </html>
   ```

6. **Test with SQLite**
   1. **Set up SQLite database**:
      ```bash
      flask db migrate -m "Connect tasks to projects"
      flask db upgrade
      ```

   2. **Run the app with development configuration**:
      ```bash
      flask run
      ```

   3. **Test your application**:
      - Add a task associated with a project (POST):
        ```bash
        curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"Test task\", \"project_id\":1}" http://localhost:5000/tasks/
        ```
      - Retrieve tasks (GET):
        ```bash
        curl http://localhost:5000/tasks/
        ```

7. **Switch to PostgreSQL Locally**
   1. **Ensure PostgreSQL is running and accessible**.

   2. **Run the app with production configuration**:
      ```bash
      flask run --config production
      ```

   3. **Run migrations for PostgreSQL**:
      ```bash
      flask db upgrade
      ```

   4. **Test your application** with PostgreSQL as you did with SQLite.

8. **Push Changes to Heroku**
   1. **Commit your changes**:
      ```bash
      git add .
      git commit -m "Connect tasks to projects"
      ```

   2. **Push to Heroku**:
      ```bash
      git push heroku feature/connect-tasks-projects:main
      ```

   3. **Run migrations on Heroku**:
      ```bash
      heroku run flask db upgrade
      ```

### Additional Information

- **Migration Commands**:
  - To create a migration: `flask db migrate -m "description"`
  - To apply a migration: `flask db upgrade`
- **Configuration Loading**: Ensure the `config.py` file reads from `config.json` to apply the appropriate settings for the environment.

### Conclusion

This document provides a step-by-step guide for connecting tasks to projects in the `feature/connect-tasks-projects` branch. It ensures that tasks can be associated with projects, enhancing the organizational capabilities of the Make-Life App.

```