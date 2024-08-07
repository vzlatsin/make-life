

# Plan to Add Selenium Tests

## Branch Name
- **Branch Name:** `feature/add-selenium-tests`

## Objective

Add end-to-end tests using Selenium to ensure that the capture functionality works correctly through the web interface, considering the different environments for local development, testing, and Heroku staging/production.

## Steps to Follow

### Step 1: Create a New Branch

1. **Create and Switch to the New Branch:**
   ```sh
   git checkout -b feature/add-selenium-tests
   ```

### Step 2: Set Up Selenium

1. **Add Selenium to `requirements.txt`:**
   - Add the Selenium dependency to your `requirements.txt` file.
   ```
   selenium
   ```

2. **Install Selenium:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver:**
   - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and ensure it is accessible in your system PATH.

### Step 3: Configure Environment for Testing

1. **Set Up Test Configuration:**
   - Ensure that the application can switch between SQLite (for local development and testing) and PostgreSQL (for Heroku staging and production).

2. **Add Environment Variables:**
   - Add environment variables for database URLs in your `.env` file.
   ```
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   DATABASE_URL_DEV=sqlite:///C:/Users/vadim/Projects/make-life/dev.db
   DATABASE_URL_TEST=sqlite:///C:/Users/vadim/Projects/make-life/test.db
   DATABASE_URL_STAGING=postgresql://vadim:223Sebastopol@localhost/makelife_db
   DATABASE_URL_PRODUCTION=postgresql://your_prod_db_username:your_prod_db_password@your_prod_db_host/your_prod_db_name
   PYTHONPATH=C:/Users/vadim/Projects/make-life
   ```

### Step 4: Write Selenium Tests

1. **Create a Test Directory (if it doesn't exist):**
   ```sh
   mkdir -p tests
   ```

2. **Create a Test File:**
   - Create a new test file named `test_capture.py` inside the `tests` directory.

3. **Write the Tests:**
   - Write tests to simulate user interactions with the `capture.html` page.

   **Test Script: `tests/test_capture.py`**
   ```python
   import unittest
   from selenium import webdriver
   from selenium.webdriver.common.by import By
   from selenium.webdriver.common.keys import Keys
   import time

   class CaptureTest(unittest.TestCase):

       def setUp(self):
           self.driver = webdriver.Chrome()

       def test_add_message(self):
           driver = self.driver
           driver.get("http://localhost:5000/capture")
           input_element = driver.find_element(By.ID, "messageInput")
           input_element.send_keys("Test message")
           input_element.send_keys(Keys.RETURN)
           time.sleep(2)  # Wait for the page to reload

           # Check if the message is added
           messages = driver.find_elements(By.CSS_SELECTOR, "#captureList .list-group-item")
           self.assertTrue(any("Test message" in message.text for message in messages))

       def test_edit_message(self):
           driver = self.driver
           driver.get("http://localhost:5000/capture")
           input_element = driver.find_element(By.ID, "messageInput")
           input_element.send_keys("Test message to edit")
           input_element.send_keys(Keys.RETURN)
           time.sleep(2)  # Wait for the page to reload

           # Edit the message
           edit_button = driver.find_element(By.CSS_SELECTOR, ".btn-edit")
           edit_button.click()
           alert = driver.switch_to.alert
           alert.send_keys("Edited test message")
           alert.accept()
           time.sleep(2)  # Wait for the page to reload

           # Check if the message is edited
           messages = driver.find_elements(By.CSS_SELECTOR, "#captureList .list-group-item")
           self.assertTrue(any("Edited test message" in message.text for message in messages))

       def test_delete_message(self):
           driver = self.driver
           driver.get("http://localhost:5000/capture")
           input_element = driver.find_element(By.ID, "messageInput")
           input_element.send_keys("Test message to delete")
           input_element.send_keys(Keys.RETURN)
           time.sleep(2)  # Wait for the page to reload

           # Delete the message
           delete_button = driver.find_element(By.CSS_SELECTOR, ".btn-delete")
           delete_button.click()
           time.sleep(2)  # Wait for the page to reload

           # Check if the message is deleted
           messages = driver.find_elements(By.CSS_SELECTOR, "#captureList .list-group-item")
           self.assertFalse(any("Test message to delete" in message.text for message in messages))

       def tearDown(self):
           self.driver.quit()

   if __name__ == "__main__":
       unittest.main()
   ```

### Step 5: Update CI/CD Pipeline

1. **Modify GitHub Actions Workflow for Testing:**
   - Update your `.github/workflows/test.yml` to include the Selenium tests.

   **Example Workflow:**
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

         - name: Run Selenium tests
           run: python -m unittest discover -s tests
   ```

### Step 6: Run the Tests Locally

1. **Ensure Your Application is Running Locally:**
   - Start your Flask application.
   ```sh
   flask run
   ```

2. **Run the Tests:**
   - Execute the test script using Python’s unittest module.
   ```sh
   python -m unittest discover -s tests
   ```

### Step 7: Commit and Push the Changes

1. **Commit the Changes:**
   ```sh
   git add requirements.txt tests/test_capture.py .github/workflows/test.yml
   git commit -m "Add Selenium tests for capture functionality"
   ```

2. **Push the Branch:**
   ```sh
   git push origin feature/add-selenium-tests
   ```

### Step 8: Create a Pull Request

1. **Create a Pull Request on GitHub:**
   - Go to your GitHub repository.
   - Create a pull request from `feature/add-selenium-tests` to `main`.
   - Describe the changes and request a review.

### Step 9: Merge the Pull Request

1. **Merge After Review:**
   - Once the pull request is reviewed and approved, merge it into the `main` branch.

### Documentation for the New Branch

Create a Markdown file to document the Selenium tests and their purpose.

**File: `selenium_tests.md`**

```markdown
# Selenium Tests for Capture Functionality

## Branch: feature/add-selenium-tests

### Objective

Add end-to-end tests using Selenium to ensure that the capture functionality works correctly through the web interface.

### Setup

1. **Install Selenium:**
   ```sh
   pip install selenium
   ```

2. **Download ChromeDriver:**
   - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and add it to your system PATH.

### Tests

The following tests are included:

1. **Add Message Test:** Verifies that a new message can be added.
2. **Edit Message Test:** Verifies that an existing message can be edited.
3. **Delete Message Test:** Verifies that a message can be deleted.

### Running the Tests

1. **Ensure Your Application is Running Locally:**
   ```sh
   flask run
   ```

2. **Run the Tests:**
   ```sh
   python -m unittest discover -s tests
   ```

### Integration with CI/CD

The Selenium tests are integrated into the GitHub Actions workflow to ensure that they are run on each push or pull request to the `main` branch.

### Conclusion

These Selenium tests help ensure that the capture functionality works correctly from the user's perspective. They simulate real user interactions and provide confidence that the application behaves as expected.
```

### Final Steps

1. **Add `selenium_tests.md` to the Branch:**
   ```sh
   git add selenium_tests.md
   git commit -m "Add documentation for Selenium tests"
   git push origin feature/add-selenium-tests
   ```

2. **Include the Documentation in the Pull Request:**
   - Ensure the `selenium_tests.md` file is included in the pull request description or linked for reviewers to read.

By following these steps, you'll have a separate branch dedicated to adding Selenium tests, along with documentation to guide others through the setup and usage of these tests. This structured approach ensures that your main branch remains stable while new tests are being developed and integrated.