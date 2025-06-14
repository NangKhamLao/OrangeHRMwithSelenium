import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def test_download_file(tmp_path):
    # Set up the Chrome options for file download
    download_dir = str(tmp_path)  # Use a temporary directory for downloads
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Set download directory
        "download.prompt_for_download": False,  # Skip the download prompt
        "safebrowsing.enabled": True,  # Allow safe downloads
    })

    # Initialize the WebDriver
    service = Service("/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service=service,options=chrome_options)

    try:
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        driver.maximize_window()

        wait = WebDriverWait(driver, 10)

        wait.until(
            EC.visibility_of_element_located((By.NAME, "username"))).send_keys("Admin")
        wait.until(
            EC.visibility_of_element_located((By.NAME, "password"))).send_keys("admin123")
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

        # Navigate to the specific page to download the file
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/104")
        time.sleep(4)
        # Find and click the download button (adjust the selector if necessary)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='oxd-icon bi-download']")))
        download_button.click()

        # Wait for the file to download
        time.sleep(5)  # Increase if the file is large

        # Verify the file exists in the download directory
        downloaded_files = os.listdir(download_dir)
        assert len(downloaded_files) > 0, "No files were downloaded."

        # Check the specific file type or name if needed
        downloaded_file_path = os.path.join(download_dir, downloaded_files[0])
        print(f"File downloaded successfully:{downloaded_file_path}")

        assert os.path.isfile(downloaded_file_path), "Downloaded file is missing."
    finally:
        # Clean up
        driver.quit() 
