import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_capture(client, clear_messages):
    # Follow the redirect for the GET request
    rv = client.get('/capture/', follow_redirects=True)
    assert rv.status_code == 200
    assert b'Capture' in rv.data  # Adjust this to match the expected content in the capture page

    # Test the POST request to /capture
    rv = client.post('/capture', data=dict(content='Test Message'), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test Message' in rv.data

def test_add_message(driver, clear_messages, start_flask_server):
    driver.get("http://localhost:5000/capture")
    input_element = driver.find_element(By.ID, "messageInput")
    input_element.send_keys("Test message")
    input_element.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the page to reload

    # Check if the message is added
    messages = driver.find_elements(By.CSS_SELECTOR, "#captureList .list-group-item")
    assert any("Test message" in message.text for message in messages)

def test_edit_message(driver, clear_messages, start_flask_server):
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
    assert any("Edited test message" in message.text for message in messages)

def test_delete_message(driver, clear_messages, start_flask_server):
    driver.get("http://localhost:5000/capture")
    input_element = driver.find_element(By.ID, "messageInput")
    input_element.send_keys("Test message to delete")
    input_element.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the page to reload

    # Wait until the delete button is clickable and then click it
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-delete"))
    )
    delete_button.click()
    time.sleep(2)  # Wait for the page to reload

    # Check if the message is deleted
    messages = driver.find_elements(By.CSS_SELECTOR, "#captureList .list-group-item")
    assert not any("Test message to delete" in message.text for message in messages)
