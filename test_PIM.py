import os.path
import time

import pytest
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.support import expected_conditions as EC

def test_add_employee(login_as_admin):
    #go to PIM module
    driver = login_as_admin
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.visibility_of_element_located((By.LINK_TEXT, "PIM"))).click()

    #click add button
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Add']"))).click()

    #first name
    wait.until(
        EC.visibility_of_element_located((By.NAME, "firstName"))).send_keys("Myint")

    #middle name
    wait.until(
        EC.visibility_of_element_located((By.NAME, "middleName"))).send_keys("Khaing")

    #last name
    wait.until(
        EC.visibility_of_element_located((By.NAME, "lastName"))).send_keys("Zin")

   #upload picture
    #1.find >> input type='file'
    #2.abspath >>os.path.abspath("file location")
    #3.send_keys

    upload_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='oxd-file-input']")))

    img_source = os.path.abspath("./resources/1.jpeg")
    upload_input.send_keys(img_source)

    #confirm image is uploaded successfully
    uploaded_pic = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "employee-image"))).get_attribute("src")
    assert "/web/images/default-photo.png" not in uploaded_pic, "image upload not successful"

    #save button
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    time.sleep(10)
    #confirm save
    url = driver.current_url
    assert "viewPersonalDetails" in url,"employee not added"

def test_edit_employee(login_as_admin):

    driver = login_as_admin
    wait = WebDriverWait(driver,10)

    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "PIM"))).click()

    action = ActionChains(driver)
    username_search = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Employee Name']/following::div")))
    action.move_to_element(username_search).click().send_keys("khaing").send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #searchbtn
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    #comfirm whether user is added in the table
    name = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Myint Khaing')]")))

    wait.until(EC.visibility_of_element_located((By.XPATH,"//i[@class='oxd-icon bi-pencil-fill']"))).click()

    assert "viewPersonalDetails" in driver.current_url, "user not exist"

    #//label[.contains(.,'License Number')]/following::div
    # driver license no
    #wait.until(EC.visibility_of_element_located(()(By.XPATH, "//form[1]/div[2]/div[2]/div[1]/div[1]/div[2]/input[1]").send_keys("1100201")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//label[contains(.,'License Number')]/following::div/input"))).send_keys("1100201")
    # license expire date
    lincesExp = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='License Expiry Date']/following::div/input")))
    lincesExp.send_keys("2024-12-12")

    # nationality
    dropdown = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Nationality']/following::div")))
    dropdown.click()
    option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text() ='Japanese']"))
    )
    option.click()

    print("Nationality Japanese selected successfully.")

    # marital status
    marital_status = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Marital Status']/following::div")))
    marital_action = ActionChains(driver)
    marital_action.move_to_element(marital_status).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    # date of birth
    dob = wait.until(EC.visibility_of_element_located((By.XPATH, "//form/div[3]/div[2]/div[1]/div/div[2]/div/div/input")))
    dob.click()
    dob.send_keys("1994-09-21")

    # gender
    '''male_radio = wait.until(EC.visibility_of_element_located(()(By.XPATH, "//label[normalize-space()='Male']")
    female_radio = wait.until(EC.visibility_of_element_located(()(By.XPATH, "//label[normalize-space()='Female']")
    if not male_radio.is_selected():
        male_radio.click()
    if not female_radio.is_selected():
        female_radio.click()'''

    radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio']")
    if len(radio_buttons) >= 2:
        radio_buttons[1].click()
    else:
        raise Exception("Radio buttons not found")

    # save button
    wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//div[@class='orangehrm-horizontal-padding orangehrm-vertical-padding']//button[@type='submit'][normalize-space()='Save']"))).click()

    success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-toast oxd-toast--success oxd-toast-container--toast']")))
    assert success_message.is_displayed(), "edit employee fail"

def test_bulk_delete_em(login_as_admin):
    driver = login_as_admin
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "PIM"))).click()

    multi_select = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='columnheader']//input[@type='checkbox']")))
    multi_select.click()

    delete_but = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Delete Selected']")))
    delete_but.click()

    time.sleep(4)
    confirm_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/div[3]/div/div/div")))
    assert confirm_msg.is_displayed(), "deleted confirm message not display"

    time.sleep(4)
    con_del = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Yes, Delete']")))
    con_del.click()

    success_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-toast-content oxd-toast-content--success']")))
    assert success_msg.is_displayed(), "Delete Failed"
