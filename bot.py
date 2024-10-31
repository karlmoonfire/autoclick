import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# URL of the ChromeDriver (set up for GitHub Actions later)
driver_path = "/usr/local/bin/chromedriver"

# Function to get a temporary email address
def get_temp_email():
    response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = response.json()[0]
    return email

# Function to get confirmation link from the inbox
def get_confirmation_link(login, domain):
    response = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
    if response.json():
        message_id = response.json()[0]['id']
        message_details = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}")
        message_body = message_details.json()['body']
        # Extract confirmation link using regex
        match = re.search(r'href="(https?://.*?)"', message_body)
        if match:
            return match.group(1)
    return None

# Function to automate sign-up
def sign_up_with_temp_email(email):
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get("https://example.com/signup")  # Replace with actual sign-up URL
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    sign_up_button = driver.find_element(By.ID, "signup-btn")  # Replace with actual element IDs
    email_input.send_keys(email)
    password_input.send_keys("your-password")
    sign_up_button.click()
    time.sleep(5)
    driver.quit()

# Function to click a button daily
def daily_button_click():
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get("https://example.com")  # Replace with actual URL
    button = driver.find_element(By.ID, "daily-button")  # Replace with actual button ID
    button.click()
    time.sleep(3)
    driver.quit()

# Main process
def main():
    temp_email = get_temp_email()
    login, domain = temp_email.split('@')
    sign_up_with_temp_email(temp_email)
    time.sleep(60)
    confirmation_link = get_confirmation_link(login, domain)
    if confirmation_link:
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get(confirmation_link)
        time.sleep(5)
        driver.quit()
    else:
        print("No confirmation email received.")

if __name__ == "__main__":
    main()
