
# Make-Life App Static Documentation

## Project Overview

Make-Life App is a web application designed for personal time management and organization. The app includes features such as a unified inbox, project management, and task tracking.

## Project Structure

```
make-life/
│
├── app/
│   ├── __init__.py          # Flask application setup
│   ├── main/                # Main blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── index.html
│   ├── inbox/               # Inbox blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   └── inbox.html
│   │   └── static/
│   │       ├── css/
│   │       │   └── inbox_style.css
│   │       └── js/
│   │           └── inbox_script.js
│   └── templates/
│       └── layout.html      # Base template
│
├── tests/                   # Test cases
│   ├── conftest.py
│   ├── inbox/
│   │   └── test_inbox.py
│   └── main/
│       └── test_main.py
│
├── docs/                    # Documentation
│   └── development_plan.md
│
├── config.py                # Configuration settings
├── run.py                   # Entry point for the app
├── run_tests.py             # Script to run tests
├── Procfile                 # Heroku deployment file
├── requirements.txt         # Dependencies
└── .gitignore               # Git ignore file
```

## Technologies and Dependencies

- **Flask**: Web framework used for the backend.
- **SQLAlchemy**: ORM for database interactions.
- **React Native**: For mobile app development.
- **SQLite**: Database for local development.

## Current Status and Next Steps

### Task: Implement Unified Inbox Feature

**Branch:** `feature/unified-inbox`

**Status:**
- Core feature implemented
- Basic UI completed
- Messages are saved to the database

