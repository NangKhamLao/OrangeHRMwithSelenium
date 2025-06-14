import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup_and_teardown():
    service = Service("/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def login_as_admin(setup_and_teardown):
    driver = setup_and_teardown
    wait = WebDriverWait(driver, 10)
    uname = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    uname.send_keys("Admin")
    password = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    password.send_keys("admin123")
    loginBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    loginBtn.click()
    return driver

