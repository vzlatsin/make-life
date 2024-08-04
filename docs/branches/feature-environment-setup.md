
### Plan

#### Objective
To implement and test changes in a development environment, followed by deployment to staging and production environments on Heroku, using a structured and tested approach.

### Detailed Plan

#### 1. Create a New Branch for Environment Setup

1. **Check out the main branch**:
   ```sh
   git checkout main
   ```

2. **Create a new branch for environment setup**:
   ```sh
   git checkout -b feature/environment-setup
   ```

#### 2. Make Changes for Environment Setup and Test Locally

1. **Update configuration files and `.env` file**:
   - Ensure your `.env` file has the correct development, testing, staging, and production database URLs.

   ```plaintext
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   DATABASE_URL_DEV=sqlite:///C:/Users/vadim/Projects/make-life/dev.db
   DATABASE_URL_TEST=sqlite:///C:/Users/vadim/Projects/make-life/test.db
   DATABASE_URL_STAGING=postgresql://vadim:223Sebastopol@localhost/makelife_db
   DATABASE_URL_PRODUCTION=postgresql://your_prod_db_username:your_prod_db_password@your_prod_db_host/your_prod_db_name
   ```

2. **Update `config.py` and `__init__.py`**:
   - Implement the environment-specific configurations.

3. **Update `conftest.py` to set the correct `PYTHONPATH`**:
   - Ensure the `PYTHONPATH` is correctly set for pytest to locate the `app` module.
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

   import pytest
   from app import create_app, db

   @pytest.fixture
   def client():
       app = create_app()
       app.config['TESTING'] = True
       with app.test_client() as client:
           yield client
   ```

4. **Ensure routes and tests are correctly aligned**:
   - Adjust the test file to ensure it aligns with the routes.
   ```python
   def test_capture(client):
       # Follow the redirect for the GET request
       rv = client.get('/capture/', follow_redirects=True)
       assert rv.status_code == 200
       assert b'Capture' in rv.data  # Adjust this to match the expected content in the capture page

       # Test the POST request to /capture
       rv = client.post('/capture', data=dict(content='Test Message'), follow_redirects=True)
       assert rv.status_code == 200
       assert b'Test Message' in rv.data
   ```

5. **Run the application locally**:
   ```sh
   set FLASK_ENV=development
   flask run
   ```

6. **Run tests locally**:
   ```sh
   set FLASK_ENV=testing
   pytest
   ```

#### 3. Push Changes for Environment Setup to GitHub

1. **Add and commit your changes**:
   ```sh
   git add .
   git commit -m "Set up environment configurations"
   ```

2. **Push changes to the remote repository**:
   ```sh
   git push origin feature/environment-setup
   ```

#### 4. Create and Configure a Staging Environment on Heroku

1. **Create a new app on Heroku for staging**:
   - Use the Heroku Dashboard or CLI to create a new Heroku app for staging:
     ```sh
     heroku create make-life-staging
     ```

2. **Add a PostgreSQL add-on to your staging app**:
   ```sh
   heroku addons:create heroku-postgresql:hobby-dev --app make-life-staging
   ```

3. **Set the environment variables for your staging app**:
   ```sh
   heroku config:set SECRET_KEY=your_secret_key JWT_SECRET_KEY=your_jwt_secret_key --app make-life-staging
   ```

#### 5. Deploy to Staging Environment

1. **Add the new Heroku remote for staging**:
   ```sh
   heroku git:remote -a make-life-staging -r heroku-staging
   ```

2. **Push your code to the staging app**:
   ```sh
   git push heroku-staging feature/environment-setup:main
   ```

3. **Run database migrations on staging**:
   ```sh
   heroku run --app make-life-staging flask db upgrade
   ```

4. **Monitor logs on staging**:
   ```sh
   heroku logs --tail --app make-life-staging
   ```

#### 6. Test in Staging Environment

1. **Access the staging application**:
   - Verify all functionalities are working as expected.

2. **Perform manual and automated testing**:
   ```sh
   heroku run --app make-life-staging pytest
   ```

#### 7. Merge Environment Setup Branch into Main

1. **Merge the environment setup branch into the main branch**:
   ```sh
   git checkout main
   git merge feature/environment-setup
   git push origin main
   ```

#### 8. Create a New Branch for Multi-User Support

1. **Create a new branch for multi-user support**:
   ```sh
   git checkout main
   git pull origin main
   git checkout -b feature/multi-user-support
   ```

2. **Implement multi-user support**:
   - Make changes and test locally as before.

3. **Push changes to GitHub and Heroku**:
   - Follow the same steps to push to GitHub and deploy to Heroku for staging.

#### 9. Test in Production Environment

1. **Access the production application**:
   - Verify all functionalities are working as expected.

2. **Monitor the application**:
   - Continuously monitor the logs for any issues.

### Summary

1. **Create specific branches for each feature**:
   - `feature/environment-setup`
   - `feature/multi-user-support`

2. **Follow the detailed steps for each branch**:
   - Make changes, test locally, push to GitHub, deploy to Heroku, and test in staging and production environments.

3. **Ensure each branch is tested and merged**:
   - After successful testing in staging, merge into the main branch.

