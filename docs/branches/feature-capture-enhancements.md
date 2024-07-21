Here is the markdown document broken down into small, testable steps:

```markdown
### Document for `feature/capture-enhancements`

#### `docs/branches/feature-capture-enhancements.md`

```markdown
# Capture Enhancements Documentation

## Branch: `feature/capture-enhancements`

### Purpose

The purpose of this branch is to enhance the capture feature by adding the ability to mark entries as handled or organized, and to include timestamps for when entries are created and when they are handled or organized. Additionally, handled or organized entries should no longer appear in the capture list.

### Steps Taken

1. **Create and Switch to a New Branch**
   - Create a new branch for capture enhancements.
   ```bash
   git checkout -b feature/capture-enhancements
   ```
   **Test:**
   - Run `git branch` and ensure `feature/capture-enhancements` is listed and active.

2. **Update the Capture Entry Model**
   - Add fields for `created_at` and `processed_at` to the `CaptureEntry` model.

   #### `app/capture/models.py`
   ```python
   from app import db
   from datetime import datetime

   class CaptureEntry(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       content = db.Column(db.String(256), nullable=False)
       handled = db.Column(db.Boolean, default=False)
       organized = db.Column(db.Boolean, default=False)
       created_at = db.Column(db.DateTime, default=datetime.utcnow)
       processed_at = db.Column(db.DateTime)
   ```
   **Test:**
   - Run `flask db migrate -m "Add timestamps to CaptureEntry model"` and `flask db upgrade`.
   - Check the database schema to ensure the `created_at` and `processed_at` fields are present.

3. **Update Routes to Handle New Fields**
   - Update routes to set `processed_at` when an entry is marked as handled or organized.

   #### `app/capture/routes.py`
   ```python
   from flask import request, jsonify, render_template
   from app.capture import capture
   from app.capture.models import db, CaptureEntry
   from datetime import datetime

   @capture.route('/<int:id>', methods=['PUT'])
   def edit_capture_entry(id):
       data = request.get_json()
       entry = CaptureEntry.query.get_or_404(id)
       entry.content = data.get('content', entry.content)
       db.session.commit()
       return jsonify({'message': 'Capture entry updated successfully!'})

   @capture.route('/<int:id>/handled', methods=['POST'])
   def handle_capture_entry(id):
       entry = CaptureEntry.query.get_or_404(id)
       entry.handled = True
       entry.processed_at = datetime.utcnow()
       db.session.commit()
       return jsonify({'message': 'Capture entry marked as handled!'})

   @capture.route('/<int:id>/organized', methods=['POST'])
   def organize_capture_entry(id):
       entry = CaptureEntry.query.get_or_404(id)
       entry.organized = True
       entry.processed_at = datetime.utcnow()
       # Additional logic to create a task from this entry
       db.session.commit()
       return jsonify({'message': 'Capture entry organized and converted to a task!'})
   ```
   **Test:**
   - Use `curl` or Postman to send POST requests to `/capture/<id>/handled` and `/capture/<id>/organized`.
   - Ensure the entries' `handled` or `organized` fields are updated, and `processed_at` is set correctly.

4. **Filter Entries in the Template**
   - Update the capture template to only show entries that are not handled or organized.

   #### `app/capture/templates/capture.html`
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Capture</title>
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
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
           <h1>Capture</h1>
           <form id="captureForm">
               <input type="text" id="captureContent" placeholder="Add a message" required>
               <button type="submit" class="btn btn-outline-success"><i class="fas fa-plus"></i> Add</button>
           </form>
           <ul id="captureList">
               {% for entry in entries %}
                   {% if not entry.handled and not entry.organized %}
                       <li>
                           {{ entry.content }}
                           <button onclick="markAsHandled({{ entry.id }})" class="btn btn-outline-primary btn-sm">Handled</button>
                           <button onclick="markAsOrganized({{ entry.id }})" class="btn btn-outline-secondary btn-sm">Organized</button>
                       </li>
                   {% endif %}
               {% endfor %}
           </ul>
       </div>
       <script>
           document.getElementById('captureForm').addEventListener('submit', function(event) {
               event.preventDefault();
               const content = document.getElementById('captureContent').value;
               fetch('/capture', {
                   method: 'POST',
                   headers: {
                       'Content-Type': 'application/json',
                   },
                   body: JSON.stringify({ content: content }),
               }).then(response => response.json())
               .then(data => {
                   if (data.message) {
                       location.reload();
                   } else {
                       alert(data.error || 'An error occurred');
                   }
               });
           });

           function markAsHandled(id) {
               fetch(`/capture/${id}/handled`, {
                   method: 'POST',
               }).then(response => response.json())
               .then(data => {
                   if (data.message) {
                       location.reload();
                   } else {
                       alert(data.error || 'An error occurred');
                   }
               });
           }

           function markAsOrganized(id) {
               fetch(`/capture/${id}/organized`, {
                   method: 'POST',
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
   **Test:**
   - Open the capture page in a browser.
   - Add a new entry and verify it appears in the list.
   - Mark the entry as handled or organized using the buttons, and verify it disappears from the list.

5. **Commit and Push Changes**
   - Commit and push the changes to the repository.

   ```bash
   git add .
   git commit -m "Enhance capture feature to handle and organize entries with timestamps"
   git push origin feature/capture-enhancements
   ```
   **Test:**
   - Run `git log` to ensure the commit appears.
   - Check the repository on GitHub or your hosting service to verify the changes are pushed.

6. **Deploy to Heroku**
   - Deploy the changes to Heroku and run migrations.

   ```bash
   git push heroku feature/capture-enhancements:main
   heroku run flask db upgrade
   ```
   **Test:**
   - Visit your Heroku app to ensure the changes are live.
   - Verify the capture feature works as expected on the deployed app.

### Conclusion

This document provides a step-by-step guide for enhancing the capture feature in the `feature/capture-enhancements` branch. It includes adding timestamps for entry creation and processing, and ensuring handled or organized entries no longer appear in the capture list.

``` 