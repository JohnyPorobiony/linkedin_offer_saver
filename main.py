from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os
load_dotenv() # <-- Load the env variables from .env file

service = Service(executable_path="C:\Development\chromedriver.exe")
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)
driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&keywords=Python%20Developer&sortBy=R")

USERNAME = os.getenv("login_linkedin")
PASSWORD = os.getenv("pass_linkedin")
PHONE_NUMBER = os.getenv("phone")

log_in = driver.find_element(By.LINK_TEXT, "Zaloguj się") # <-- In Poland only
log_in.click()

username_fill = driver.find_element(By.ID, "username")
username_fill.send_keys(USERNAME)

password_fill = driver.find_element(By.ID, "password")
password_fill.send_keys(PASSWORD)
password_fill.send_keys(Keys.ENTER)

input() # Pause to pass anti-bot verification

n = 0
while True:
    # For some reason driver finds only few first offers IDs so it is required to keep finding new offers as we load new pages.
    offers_ids = [offer.get_attribute("data-job-id") for offer in driver.find_elements(By.CLASS_NAME, "job-card-container")]

    driver.get(f"https://www.linkedin.com/jobs/search/?currentJobId={offers_ids[n]}&f_AL=true&keywords=Python%20Developer&sortBy=R")

    # Give the page some time to load. It may also be possible to use time.sleep(), but it should be avoided.
    save = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jobs-save-button"))).click()
                                                         
    print(f"Offer #{offers_ids[n]} saved")

    n += 1
