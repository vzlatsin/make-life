### Document for `feature/gtd-projects`

#### `docs/branches/feature-gtd-projects.md`

```markdown
# GTD Projects Functionality Documentation

## Branch: `feature/gtd-projects`

### Purpose

The purpose of this branch is to add the functionality of managing projects as per the GTD (Getting Things Done) methodology. This will allow users to organize tasks into projects, providing better organization and tracking.

### Steps Taken

1. **Create and Switch to a New Branch**
   - We create a new branch for adding the projects functionality to keep changes organized.
   ```bash
   git checkout -b feature/gtd-projects
   ```

2. **Define the Project Model**
   - Add the project model to `app/models.py`.

   #### `app/models.py`
   ```python
   from app import db

   class Project(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(128), nullable=False)
       description = db.Column(db.Text)
       status = db.Column(db.String(64))
       due_date = db.Column(db.Date)
       tasks = db.relationship('Task', backref='project', lazy=True)

   class Task(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       content = db.Column(db.String(256), nullable=False)
       project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
       # other fields...
   ```

3. **Create the Database Migration**
   - Generate and apply the migration for the new project model.

   ```bash
   flask db migrate -m "Add Project model"
   flask db upgrade
   ```

4. **Implement Routes and Views**
   - Add the routes for managing projects in a new `projects` blueprint.

   **Create a new blueprint for projects:**

   Create `app/projects/routes.py` and add the following:

   #### `app/projects/routes.py`
   ```python
   from flask import Blueprint, render_template, redirect, url_for, request, flash
   from app import db
   from app.models import Project
   from app.projects.forms import ProjectForm

   projects = Blueprint('projects', __name__)

   @projects.route('/projects', methods=['GET'])
   def get_projects():
       projects = Project.query.all()
       return render_template('projects/projects.html', projects=projects)

   @projects.route('/projects/add', methods=['GET', 'POST'])
   def add_project():
       form = ProjectForm()
       if form.validate_on_submit():
           project = Project(name=form.name.data, description=form.description.data,
                             status=form.status.data, due_date=form.due_date.data)
           db.session.add(project)
           db.session.commit()
           flash('Project added successfully', 'success')
           return redirect(url_for('projects.get_projects'))
       return render_template('projects/add_project.html', form=form)

   @projects.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
   def edit_project(project_id):
       project = Project.query.get_or_404(project_id)
       form = ProjectForm(obj=project)
       if form.validate_on_submit():
           project.name = form.name.data
           project.description = form.description.data
           project.status = form.status.data
           project.due_date = form.due_date.data
           db.session.commit()
           flash('Project updated successfully', 'success')
           return redirect(url_for('projects.get_projects'))
       return render_template('projects/edit_project.html', form=form, project=project)

   @projects.route('/projects/delete/<int:project_id>', methods=['POST'])
   def delete_project(project_id):
       project = Project.query.get_or_404(project_id)
       db.session.delete(project)
       db.session.commit()
       flash('Project deleted successfully', 'success')
       return redirect(url_for('projects.get_projects'))
   ```

   **Register the blueprint in `app/__init__.py`:**

   #### `app/__init__.py`
   ```python
   from app.projects.routes import projects as projects_blueprint
   app.register_blueprint(projects_blueprint, url_prefix='/projects')
   ```

5. **Add Templates**
   - Create the necessary templates for listing, adding, editing, and deleting projects in `app/templates/projects/`.

   **projects.html:**
   ```html
   {% extends "base.html" %}
   {% block content %}
       <h1>Projects</h1>
       <a href="{{ url_for('projects.add_project') }}">Add Project</a>
       <ul>
           {% for project in projects %}
               <li>{{ project.name }} - {{ project.status }} - <a href="{{ url_for('projects.edit_project', project_id=project.id) }}">Edit</a> - <form action="{{ url_for('projects.delete_project', project_id=project.id) }}" method="POST"><button type="submit">Delete</button></form></li>
           {% endfor %}
       </ul>
   {% endblock %}
   ```

   **add_project.html:**
   ```html
   {% extends "base.html" %}
   {% block content %}
       <h1>Add Project</h1>
       <form method="POST">
           {{ form.hidden_tag() }}
           {{ form.name.label }} {{ form.name(size=32) }}<br>
           {{ form.description.label }} {{ form.description(rows=4, cols=32) }}<br>
           {{ form.status.label }} {{ form.status(size=32) }}<br>
           {{ form.due_date.label }} {{ form.due_date() }}<br>
           <button type="submit">Add Project</button>
       </form>
   {% endblock %}
   ```

   **edit_project.html:**
   ```html
   {% extends "base.html" %}
   {% block content %}
       <h1>Edit Project</h1>
       <form method="POST">
           {{ form.hidden_tag() }}
           {{ form.name.label }} {{ form.name(size=32) }}<br>
           {{ form.description.label }} {{ form.description(rows=4, cols=32) }}<br>
           {{ form.status.label }} {{ form.status(size=32) }}<br>
           {{ form.due_date.label }} {{ form.due_date() }}<br>
           <button type="submit">Update Project</button>
       </form>
   {% endblock %}
   ```

6. **Test the Project Functionality**
   - Run the application and test adding, editing, deleting, and listing projects.

   ```bash
   flask run
   ```

   - Add a project through the web interface and verify it appears in the list.
   - Edit a project and ensure the changes are saved.
   - Delete a project and ensure it is removed from the list.

7. **Push Changes to Remote Repository**
   1. **Commit your changes**:
      ```bash
      git add .
      git commit -m "Add GTD project functionality"
      ```

   2. **Push to remote repository**:
      ```bash
      git push origin feature/gtd-projects
      ```

### Additional Information

- **Database Migration**:
  - To create a migration: `flask db migrate -m "description"`
  - To apply a migration: `flask db upgrade`

### Conclusion

This document provides a step-by-step guide for adding the GTD project functionality in the `feature/gtd-projects` branch. It enables users to manage projects and organize tasks more effectively within the Make-Life application.
```