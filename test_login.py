import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



@pytest.mark.parametrize("username, password, expected", [
    ("Admin", "admin123", True),
    ("Admin", "admin", False),
    ("admin", "admin123", False),
    ("aaaaa", "aaaaa", False),

])

def test_login(username, password, expected,setup_and_teardown):
    driver = setup_and_teardown
    # driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)
    uname = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    uname.send_keys(username)
    pword = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pword.send_keys(password)
    loginbtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    loginbtn.click()
    time.sleep(5)

    if expected:
        assert "dashboard" in driver.current_url, "login failed with valid credential"
    else:
        err_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='alert']")))
        assert "Invalid credentials" in err_msg.text, "login successful with invalid credential"


#valid username , valid password, true
#valid username, invalid password, false
#invalid username, valid password, fasle
#invalid username, invalid password, false
#no username, no password, false
def test_required_field_login(setup_and_teardown):
   pass
def test_forgot_password(setup_and_teardown):
    pass

def test_logout(login_as_admin):
    driver = login_as_admin
    wait = WebDriverWait(driver,10)
    #click user icon
    user_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='oxd-userdropdown-name']")))
    user_icon.click()

    #click log out button
    logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Logout']")))
    logout_btn.click()

    #confirm logout
    assert "login" in driver.current_url, "logout failed"

