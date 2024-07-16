from flask import request, jsonify, render_template
from app.inbox import inbox
from app.inbox.models import db, InboxEntry
import os

print("Loading inbox routes...")  # Debug print statement

@inbox.route('/', methods=['POST'])
def add_inbox_entry():
    print("POST request received")  # Debug print statement
    data = request.get_json()
    print(f"Received data: {data}")  # Debug print statement
    content = data.get('content')
    if content:
        entry = InboxEntry(content=content)
        db.session.add(entry)
        db.session.commit()
        print("Entry added to database")  # Debug print statement
        return jsonify({'message': 'Entry added successfully!'}), 201
    print("Content is required")  # Debug print statement
    return jsonify({'error': 'Content is required!'}), 400

@inbox.route('/', methods=['GET'])
def get_inbox_entries():
    try:
        print("GET request received")  # Debug print statement
        entries = InboxEntry.query.all()
        print(f"Entries retrieved: {[entry.content for entry in entries]}")  # Debug print statement
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'inbox.html')
        print(f"Rendering template at path: {template_path}")  # Debug print statement
        return render_template('inbox.html', messages=entries)
    except Exception as e:
        print(f"Error retrieving entries: {e}")  # Debug print statement
        return str(e), 500

@inbox.route('/<int:id>', methods=['DELETE'])
def delete_inbox_entry(id):
    print("DELETE request received")  # Debug print statement
    entry = InboxEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    print("Entry deleted from database")  # Debug print statement
    return jsonify({'message': 'Entry deleted successfully!'}), 200
