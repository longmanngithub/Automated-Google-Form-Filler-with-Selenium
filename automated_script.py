import random
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Logging Configuration ===
logging.basicConfig(
    filename="/home/long/Desktop/log.txt", # Log file path
    level=logging.INFO, # Set logging level to INFO
    format='%(asctime)s - %(message)s' # Log format with timestamp
)

# Declare your randomized variables here if needed

# === Randomized Data ===
genders = ['Male', 'Female', 'Prefer not to say']
currencies = ['USD (US Dollar)', 'KHR (Khmer Riel)']
spending_estimates = {
    'USD (US Dollar)': ['45', '50', '60', '70', '80', '90', '100', '150', '175', '200', '250', '300', '325', '350', '375', '400', '425', '450', '500', '550'],
    'KHR (Khmer Riel)': ['160000', '180000', '250000', '200000', '300000', '280000', '320000', '350000', '400000', '450000', '500000', '600000', '800000', '1000000', '1500000', '2000000']
}
satisfaction_levels = ['4', '5', '6', '7', '8', '9', '10']

# END OF DECLARATION

# === Chrome Options for Raspberry Pi ===
def get_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser" # Must be in /usr/bin for Raspberry Pi
    options.add_argument("--headless") # Run in headless mode
    options.add_argument("--no-sandbox") # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
    options.add_argument("--disable-gpu") # Disable GPU hardware acceleration

    return webdriver.Chrome(options=options) # Initialize the Chrome driver with the specified options

# === Open Google Form ===
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe4xjo27-dRzIDzFI71iDjtQWmZk2F6imfmVx43XvmWzmp7BQ/viewform?hl=en" # Replace with your form URL

# === Automation Function ===
def submit_form(driver):
    driver.get(form_url)
    time.sleep(2)

    # Section 1 - Checkbox
    driver.find_element(By.XPATH, "//div[@role='checkbox']").click() # Click the consent checkbox
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Next']").click() # Click the "Next" button
    time.sleep(2)

    # Section 2 - Age and Gender
    age = str(random.randint(18, 25))
    gender = random.choice(genders)
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys(age) # Fill the age input
    driver.find_element(By.XPATH, f"//div[@data-value='{gender}']").click() # Click the gender option
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Next']").click() # Click the "Next" button
    time.sleep(2)

    # Section 3 - Currency and Spending
    currency = random.choice(currencies)
    amount = random.choice(spending_estimates[currency])

    # Wait for the currency option to load before clicking
    currency_radio = WebDriverWait(driver, 10).until( 
        EC.element_to_be_clickable((By.XPATH, f"//div[@data-value='{currency}']")) # Wait for the currency radio button to be clickable
    )
    driver.execute_script("arguments[0].click();", currency_radio) # Click the currency option using JavaScript to avoid click issues

    time.sleep(2)

    # Fill the short answer input
    short_answers = driver.find_elements(By.XPATH, "//input[@type='text']") # Get all short answer inputs
    short_answers[1].send_keys(amount) # Fill the spending estimate

    # Click "Next"
    driver.find_element(By.XPATH, "//span[text()='Next']").click() # Click the "Next" button
    time.sleep(2)

    # Section 4 - Satisfaction (Linear scale) with retry
    rating = random.choice(satisfaction_levels)
    rating_xpath = f"//div[@data-value='{rating}']" # XPath for the satisfaction rating

    # Retry clicking the satisfaction rating
    for attempt in range(3):
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, rating_xpath))).click() # Wait for the rating to be clickable
            time.sleep(1)
            break  # success, exit retry loop
        # If the click fails, log the error and retry
        except Exception as e:
            print(f"[Retry {attempt+1}/3] Could not click rating {rating}: {e}")
            time.sleep(2)
    # If all retries fail, log the error and skip this form submission
    else:
        print("Max retries reached for satisfaction rating. Skipping this form.")
        driver.refresh() # Refresh the form to start over
        return

    # Proceed to submit
    time.sleep(1)

    # Click the "Submit" button
    try:
        submit_button = WebDriverWait(driver, 10).until( # Wait for the submit button to be present
            EC.presence_of_element_located((By.XPATH, "//span[text()='Submit']")) # Locate the submit button
        )
        if submit_button.is_displayed() and submit_button.is_enabled(): # Check if the submit button is clickable
            submit_button.click()
        else: # If the submit button is present but not clickable
            logging.warning("Submit button is present but not clickable.")
            return
    except Exception as e: # If the submit button is not found or not clickable
        logging.warning(f"Submit button not found or not clickable: {e}")
        return  # Skip this submission

# === Main Loop: 8 AM to 10 PM ===
if __name__ == "__main__":
    driver = get_driver()
    try:
        while True:
            now = datetime.now() # Get the current time
            # Check if the current time is between 8 AM and 10 PM
            if 8 <= now.hour < 22: 
                submit_form(driver) # Submit the form
                wait_minutes = random.randint(5, 60) # Random wait time between 5 and 60 minutes
                logging.info(f"[{now.strftime('%H:%M:%S')}] Submitted. Waiting {wait_minutes} minutes...") # Log the submission time and wait duration
                time.sleep(wait_minutes * 60)
            # If the current time is outside the range, sleep for 10 minutes
            else:
                logging.info(f"[{now.strftime('%H:%M:%S')}] Outside 8 AM -10 PM. Sleeping 10 minutes.") # Log the time and sleep duration
                time.sleep(600)
    # Handle keyboard interrupt to stop the script
    except KeyboardInterrupt:
        print("Stopped by user.")
        driver.quit()
