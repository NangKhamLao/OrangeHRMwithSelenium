import time

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

@pytest.mark.parametrize("username, password, confirm_password, expected_message",[
    #positive test case: valid input
    ("lily1","admin123","admin123",[]),
    #negative test case, password should have at least 7 character
    ("lily2","admin", "admin", ["Should have at least 7 characters"]),
    #username should have 5 character
    ("lily","admin123","admin123",["Should be at least 5 characters"]),
    #password do not match
    ("lily3","admin123","admin124",["Passwords do not match"]),
    #required
    ("","","",["Required"]),
    #
])
def test_add_admin(login_as_admin,username,password,confirm_password, expected_message):
    driver = login_as_admin
    wait = WebDriverWait(driver,10)
    admin_tab = wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"Admin")))
    admin_tab.click()

    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Add ']")))
    add_btn.click()

    #user role
    user_role = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='User Role']/following::div[1]")))
    action_role = ActionChains(driver)
    action_role.move_to_element(user_role).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #employee name
    emp_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']")))
    emp_name.send_keys("a")
    time.sleep(5)
    action_emp = ActionChains(driver)
    action_emp.move_to_element(emp_name).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #status
    action_status = ActionChains(driver)
    status = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Status']/following::div[1]")))
    action_status.move_to_element(status).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #username
    user_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Username']/following::div[1]//input")))
    user_name.send_keys(username)
    #password
    pass_word = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Password']/following::div[1]//input")))
    pass_word.send_keys(password)

    #confirm password
    con_pas = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Confirm Password']/following::div[1]//input")))
    con_pas.send_keys(confirm_password)

    #save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    save_btn.click()

    #if expected error occur, verify validation message
    if expected_message:
        for error in expected_message:
            error_msg = wait.until(EC.visibility_of_element_located((By.XPATH,f"//span[normalize-space()='Should have at least 7 char']")))
            assert error_msg.is_displayed(),"Expected error message is not display"
    else:
        success_msg =  wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Successfully')]"))
    )
        assert success_msg.is_displayed(), "Admin user not added successfully"

def test_search_admin(login_as_admin):
    driver = login_as_admin
    wait = WebDriverWait(driver, 10)
    admin_tab = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Admin")))
    admin_tab.click()

    add_name = "lily1"
    username = wait.until(EC.visibility_of_element_located((By.XPATH,"//label[text()='Username']/following::div//input")))
    username.send_keys(add_name)

    #form
    form = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"oxd-form")))
    form.submit()

    #confirm whether user exists
    name = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{add_name}')")))
    assert name.is_displayed(), "user not added sucessfully"

    edit_icon = wait.until(EC.visibility_of_element_located((By.XPATH, "//i[@class='oxd-icon bi-pencil-fill']")))
    edit_icon.click()

    change_name = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Username']/following::div[1]//input")))
    change_name.send_keys("Lily Rose")

    change_password = wait.until(EC.visibility_of_element_located((By.XPATH,"//i[@class='oxd-icon bi-check oxd-checkbox-input-icon']")))
    change_password.click()

    # password
    pass_word = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Password']/following::div[1]//input")))
    pass_word.send_keys("password123")

    # confirm password
    con_pas = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Confirm Password']/following::div[1]//input")))
    con_pas.send_keys("password123")

    save_btn = wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()=' Save ']")))
    save_btn.click()
    success_msg = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Successfully')]"))
    )
    assert success_msg.is_displayed(), "Admin user not added updated"

def delete_admin():
    assert True