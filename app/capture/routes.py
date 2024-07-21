from flask import request, jsonify, render_template
from app.capture import capture
from app.capture.models import db, CaptureEntry
import os

print("Loading capture routes...")  # Debug print statement

@capture.route('/', methods=['POST'])
def add_capture_entry():
    print("POST request received")  # Debug print statement
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    print(f"Received data: {data}")  # Debug print statement
    content = data.get('content')
    if content:
        entry = CaptureEntry(content=content)
        db.session.add(entry)
        db.session.commit()
        print("Entry added to database")  # Debug print statement
        return jsonify({'message': 'Entry added successfully!'}), 201
    print("Content is required")  # Debug print statement
    return jsonify({'error': 'Content is required!'}), 400

@capture.route('/', methods=['GET'])
def get_capture_entries():
    try:
        print("GET request received")  # Debug print statement
        entries = CaptureEntry.query.all()
        print(f"Entries retrieved: {[entry.content for entry in entries]}")  # Debug print statement
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'capture.html')
        print(f"Rendering template at path: {template_path}")  # Debug print statement
        return render_template('capture.html', messages=entries)
    except Exception as e:
        print(f"Error retrieving entries: {e}")  # Debug print statement
        return str(e), 500

@capture.route('/<int:id>', methods=['DELETE'])
def delete_capture_entry(id):
    print("DELETE request received")  # Debug print statement
    entry = CaptureEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    print("Entry deleted from database")  # Debug print statement
    return jsonify({'message': 'Entry deleted successfully!'}), 200
