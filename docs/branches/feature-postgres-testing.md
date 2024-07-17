### Document for `feature/postgres-testing`

#### `docs/branches/feature-postgres-testing.md`

```markdown
# PostgreSQL Testing Documentation

## Branch: `feature/postgres-testing`

### Purpose

The purpose of this branch is to test the Make-Life App with a PostgreSQL database to ensure compatibility and functionality in a production-like environment.

### Steps Taken

1. **Create and Switch to a New Branch**
   - Create a new branch for PostgreSQL testing to keep changes organized.
   ```bash
   git checkout -b feature/postgres-testing
   ```

2. **Ensure Configuration Files for PostgreSQL**

   - Ensure `config.py` and `config_private.py` are correctly set up for PostgreSQL.

   #### `config.py`
   ```python
   import os

   basedir = os.path.abspath(os.path.dirname(__file__))

   class Config:
       SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
       SQLALCHEMY_TRACK_MODIFICATIONS = False

   class PostgresConfig(Config):
       try:
           from config_private import PostgresConfig as PrivateConfig
           SQLALCHEMY_DATABASE_URI = PrivateConfig.SQLALCHEMY_DATABASE_URI
       except ImportError:
           SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'

   class TestConfig(Config):
       TESTING = True
       SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
   ```

   #### `config_private.py`
   ```python
   class PostgresConfig:
       SQLALCHEMY_DATABASE_URI = 'postgresql://vadim:223Sebastopol@localhost/makelife_db'
       SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```

3. **Set Up PostgreSQL Locally**
   - Ensure PostgreSQL is installed, running, and accessible locally.

4. **Run the Application with PostgreSQL Configuration**

   - Set the `FLASK_CONFIG` environment variable to use `config.PostgresConfig`.

   ```bash
   export FLASK_CONFIG=config.PostgresConfig
   ```

   - Alternatively, modify the `run.py` file to accept a configuration parameter.

   #### `run.py`
   ```python
   import os
   import sys
   from app import create_app

   config_name = 'config.Config'  # Default to development
   if len(sys.argv) > 1:
       config_name = sys.argv[1]

   app = create_app(config_name)

   if __name__ == '__main__':
       app.run(debug=(config_name == 'config.Config'))
   ```

   - Run the app with PostgreSQL configuration.
   ```bash
   python run.py config.PostgresConfig
   ```

5. **Run Database Migrations for PostgreSQL**
   - Initialize and run migrations to set up the PostgreSQL database schema.
   ```bash
   flask db upgrade
   ```

6. **Test the Application with PostgreSQL**
   - Add an entry (POST):
     ```bash
     curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"Test entry\"}" http://localhost:5000/inbox/
     ```
   - Retrieve entries (GET):
     ```bash
     curl http://localhost:5000/inbox/
     ```
   - Delete an entry (DELETE):
     ```bash
     curl -X DELETE http://localhost:5000/inbox/1
     ```

7. **Push Changes to Heroku**
   1. **Commit your changes**:
      ```bash
      git add .
      git commit -m "Tested with PostgreSQL"
      ```

   2. **Push to Heroku**:
      ```bash
      git push heroku feature/postgres-testing:main
      ```

   3. **Run migrations on Heroku**:
      ```bash
      heroku run flask db upgrade
      ```

### Additional Information

- **Migration Commands**:
  - To create a migration: `flask db migrate -m "description"`
  - To apply a migration: `flask db upgrade`
- **Configuration Loading**: The `config.py` file reads from `config_private.py` to apply the appropriate settings for the environment.

### Conclusion

This document provides a step-by-step guide for testing the Make-Life App with PostgreSQL in the `feature/postgres-testing` branch. It ensures that the application can switch between SQLite and PostgreSQL seamlessly, allowing for flexible and reliable development and deployment.

```
