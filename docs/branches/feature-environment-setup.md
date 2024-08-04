
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

1. **Update configuration files and .env file**:
   - Ensure your `.env` file has the correct development, testing, staging, and production database URLs.

2. **Update `config.py` and `__init__.py`**:
   - Implement the environment-specific configurations.

3. **Run the application locally**:
   ```sh
   export FLASK_ENV=development
   flask run
   ```

4. **Run tests locally**:
   ```sh
   export FLASK_ENV=testing
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
   - Follow the steps to create a new Heroku app for staging.

2. **Set the environment variables for your staging app**:
   - Add the necessary environment variables for staging.

3. **Create a user and database in the staging PostgreSQL database**:
   - Follow the steps to create a new user and database in PostgreSQL for staging.

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

