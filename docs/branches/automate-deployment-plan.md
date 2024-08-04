
### Plan to Automate Deployment Process

#### Step 1: Set Up GitHub Actions for Continuous Integration (CI)

1. **Create a GitHub Actions Workflow:**
   - Create a `.github/workflows/test.yml` file in your repository.

2. **Configure CI Workflow:**
   - Define a workflow that runs tests when code is pushed or a pull request is made.

```yaml
name: Run Tests

on:
  push:
    branches:
      - main
      - 'feature/**'
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:latest
        ports:
          - 5432:5432
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
          pip install psycopg2-binary

      - name: Run tests
        env:
          DATABASE_URL: postgresql://user:password@localhost:5432/test_db
        run: |
          flask db upgrade
          pytest
```

3. **Test CI Workflow:**
   - Push changes to a feature branch and verify that tests run successfully.

#### Step 2: Set Up GitHub Actions for Continuous Deployment (CD) to Staging

1. **Create a Staging Deployment Workflow:**
   - Create a `.github/workflows/deploy_staging.yml` file in your repository.

2. **Configure CD Workflow for Staging:**
   - Define a workflow that deploys to staging when code is merged into the `main` branch.

```yaml
name: Deploy to Staging

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
          HEROKU_APP_NAME: make-life-staging
        run: |
          git remote add heroku https://git.heroku.com/${{ env.HEROKU_APP_NAME }}.git
          git push heroku main
```

3. **Test CD Workflow for Staging:**
   - Merge a feature branch into `main` and verify that the app is deployed to the staging environment.

#### Step 3: Set Up GitHub Actions for Continuous Deployment (CD) to Production

1. **Create a Production Deployment Workflow:**
   - Create a `.github/workflows/deploy_production.yml` file in your repository.

2. **Configure CD Workflow for Production:**
   - Define a workflow that deploys to production when a GitHub release is created.

```yaml
name: Deploy to Production

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
          HEROKU_APP_NAME: make-life
        run: |
          git remote add heroku https://git.heroku.com/${{ env.HEROKU_APP_NAME }}.git
          git push heroku main
```

3. **Test CD Workflow for Production:**
   - Create a GitHub release and verify that the app is deployed to the production environment.

### Summary

By following these steps, you will have an automated CI/CD pipeline that:

1. Runs tests on each push and pull request.
2. Deploys to the staging environment when code is merged into the `main` branch.
3. Deploys to the production environment when a GitHub release is created.

Each step is small, testable, and ensures the process is robust and reliable.