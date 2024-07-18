### Document for `feature/configuration-setup`

#### `docs/branches/feature-configuration-setup.md`

```markdown
# Configuration Setup Documentation

## Branch: `feature/configuration-setup`

### Purpose

The purpose of this branch is to set up the configuration for the Make-Life App to use different databases for different environments (development with SQLite, production with PostgreSQL).

### Steps Taken

1. **Create and Switch to a New Branch**
   - We create a new branch for the configuration setup to keep changes organized.
   ```bash
   git checkout -b feature/configuration-setup
   ```

2. **Create Configuration Files**
   - Create `config.json` to hold configuration settings for different environments.

   #### `config.json`
   ```json
   {
       "development": {
           "SECRET_KEY": "your_secret_key",
           "SQLALCHEMY_DATABASE_URI": "sqlite:///app.db",
           "SQLALCHEMY_TRACK_MODIFICATIONS": false
       },
       "production": {
           "SECRET_KEY": "your_secret_key",
           "SQLALCHEMY_DATABASE_URI": "postgresql://vadim:223Sebastopol@localhost/makelife_db",
           "SQLALCHEMY_TRACK_MODIFICATIONS": false
       }
   }
   ```

3. **Update `config.py`**
   - Update `config.py` to read from the configuration file.

   #### `config.py`
   ```python
   import os
   import json

   class Config:
       SECRET_KEY = None
       SQLALCHEMY_DATABASE_URI = None
       SQLALCHEMY_TRACK_MODIFICATIONS = False

   def load_config(config_name):
       with open('config.json') as config_file:
           config_data = json.load(config_file)
           env_config = config_data.get(config_name, {})
           for key, value in env_config.items():
               setattr(Config, key, value)
       return Config
   ```

4. **Update `create_app` Function**
   - Modify `create_app` function in `app/__init__.py`.

   #### `app/__init__.py`
   ```python
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_migrate import Migrate
   import os
   from config import load_config

   db = SQLAlchemy()
   migrate = Migrate()

   def create_app(config_name='development'):
       template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
       static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

       app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
       config = load_config(config_name)
       app.config.from_object(config)

       db.init_app(app)
       migrate.init_app(app, db)

       from .main import main as main_blueprint
       from .inbox import inbox as inbox_blueprint

       app.register_blueprint(main_blueprint)
       app.register_blueprint(inbox_blueprint, url_prefix='/inbox')

       print("Registered routes:")
       for rule in app.url_map.iter_rules():
           print(f"{rule} -> {rule.endpoint}")

       return app
   ```

5. **Modify `run.py`**
   - Modify `run.py` to accept a configuration name.

   #### `run.py`
   ```python
   import os
   import sys
   from app import create_app

   config_name = 'development'  # Default to development
   if len(sys.argv) > 1:
       config_name = sys.argv[1]

   app = create_app(config_name)

   if __name__ == '__main__':
       app.run(debug=(config_name == 'development'))
   ```

6. **Test with SQLite**
   1. **Set up SQLite database**:
      ```bash
      flask db init
      flask db migrate -m "Initial migration"
      flask db upgrade
      ```

   2. **Run the app with development configuration**:
      ```bash
      python run.py development
      ```

   3. **Test your application**:
      - Add an entry (POST):
        ```bash
        curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"Test entry\"}" http://localhost:5000/inbox/
        ```
      - Retrieve entries (GET):
        ```bash
        curl http://localhost:5000/inbox/
        ```

7. **Switch to PostgreSQL Locally**
   1. **Install and set up PostgreSQL**:
      Ensure PostgreSQL is running and accessible.

   2. **Run the app with production configuration**:
      ```bash
      python run.py production
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
      git commit -m "Setup configuration and tested with PostgreSQL"
      ```

   2. **Push to Heroku**:
      ```bash
      git push heroku feature/configuration-setup:main
      ```

   3. **Run migrations on Heroku**:
      ```bash
      heroku run flask db upgrade
      ```

### Additional Information

- **Migration Commands**:
  - To create a migration: `flask db migrate -m "description"`
  - To apply a migration: `flask db upgrade`
- **Configuration Loading**: The `config.py` file reads from `config.json` to apply the appropriate settings for the environment.

### Conclusion

This document provides a step-by-step guide for setting up the configuration in the `feature/configuration-setup` branch. It ensures that the application can switch between SQLite and PostgreSQL seamlessly, allowing for flexible and reliable development and deployment.

```