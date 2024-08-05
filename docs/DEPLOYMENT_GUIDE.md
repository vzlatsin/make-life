
# High-Level Deployment Guide for Administrators

## Introduction

This guide provides an overview of the deployment process for the `make-life` application. It outlines the tools and workflows used to ensure a smooth and successful deployment to both staging and production environments.

## Tools and Technologies

- **GitHub**: Source code repository and CI/CD workflow management.
- **GitHub Actions**: CI/CD tool integrated with GitHub to automate the deployment process.
- **Heroku**: Platform-as-a-Service (PaaS) used for deploying and managing the application.
- **Python**: Programming language used for the application.
- **pip**: Python package installer used to manage dependencies.

## Deployment Environments

- **Staging**: Used for testing new features before they are released to production. Deployed on Heroku with the `make-life-staging` app.
- **Production**: The live environment for end-users. Deployed on Heroku with the `make-life` app.

## Deployment Process Overview

### 1. Code Commit and Push

- Developers commit and push their changes to the `main` branch on GitHub.
- Ensure the code is up-to-date and all changes are properly committed.

### 2. Continuous Integration (CI)

- **GitHub Actions** triggers automated tests on each push to the `main` branch.
- The CI workflow is defined in `.github/workflows/test.yml`.

```yaml
name: Run Tests

on:
  push:
    branches:
      - main

jobs:
  test:
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
          pip install pytest

      - name: Run tests
        run: pytest
```

### 3. Deployment to Staging

- After successful tests, the code is deployed to the staging environment.
- The deployment workflow is defined in `.github/workflows/deploy_staging.yml`.

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
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Configure Git user
        run: |
          git config --global user.email "vadim@example.com"
          git config --global user.name "Vadim Zlatsin"

      - name: Add Heroku remote
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git remote add heroku https://heroku:$HEROKU_API_KEY@git.heroku.com/make-life-staging.git

      - name: Fetch all branches and tags
        run: |
          git fetch --all

      - name: Ensure main branch is checked out
        run: |
          git checkout -b main origin/main || git checkout main

      - name: Sanity Check - Local Branches
        run: |
          echo "Sanity check - local branches:"
          git branch

      - name: Sanity Check - Remote Branches
        run: |
          echo "Sanity check - remote branches:"
          git branch -r

      - name: Merge Heroku main with --allow-unrelated-histories
        run: |
          git merge heroku/main --allow-unrelated-histories || git merge --abort

      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git push heroku main
```

### 4. Deployment to Production

- Once the changes are verified in staging, a new release is created on GitHub to trigger the production deployment.
- The production deployment workflow is defined in `.github/workflows/deploy_production.yml`.

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
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Configure Git user
        run: |
          git config --global user.email "vadim@example.com"
          git config --global user.name "Vadim Zlatsin"

      - name: Add Heroku remote
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git remote add heroku https://heroku:$HEROKU_API_KEY@git.heroku.com/make-life.git

      - name: Fetch all branches and tags
        run: |
          git fetch --all

      - name: Ensure main branch is checked out
        run: |
          git checkout -b main origin/main || git checkout main

      - name: Sanity Check - Local Branches
        run: |
          echo "Sanity check - local branches:"
          git branch

      - name: Sanity Check - Remote Branches
        run: |
          echo "Sanity check - remote branches:"
          git branch -r

      - name: Merge Heroku main with --allow-unrelated-histories
        run: |
          git merge heroku/main --allow-unrelated-histories || git merge --abort

      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git push heroku main
```

### Key Considerations

- **Environment Variables:** Ensure that all necessary environment variables and secrets (such as `HEROKU_API_KEY`) are correctly configured in GitHub Secrets.
- **Sanity Checks:** The workflow includes sanity checks to ensure that the branches are consistent before pushing to Heroku.
- **Monitoring:** Regularly monitor the deployments and application performance using Heroku's monitoring tools.

### Conclusion

This guide provides a high-level overview of the deployment process for the `make-life` application. By following these steps and workflows, you can ensure a smooth and successful deployment to both staging and production environments. If you encounter any issues or have questions, please refer to the documentation or seek assistance from the development team.


