import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Declare your randomized variables here

# === Randomized Data ===
genders = ['Male', 'Female', 'Prefer not to say']
currencies = ['USD (US Dollar)', 'KHR (Khmer Riel)']
spending_estimates = {
    'USD (US Dollar)': ['20', '30', '40', '45', '50', '60', '70', '80', '90', '100', '150'],
    'KHR (Khmer Riel)': ['40000', '80000', '160000', '180000', '250000', '200000', '300000', '280000', '320000', '350000', '400000']
}
satisfaction_levels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

# END OF DECLARATION

# === Setup WebDriver ===
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# === Open Google Form ===
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe4xjo27-dRzIDzFI71iDjtQWmZk2F6imfmVx43XvmWzmp7BQ/viewform?hl=en" # Replace with your form URL
driver.get(form_url)
time.sleep(2)

# === Infinite Submission Loop ===
try:
    while True:
        driver.get(form_url) # Reload the form for each submission
        time.sleep(2)

        # FEEL FREE TO ADJUST THE SCRIPT BELOW TO MATCH YOUR FORM'S STRUCTURE

        # Section 1: Consent
        driver.find_element(By.XPATH, "//div[@role='checkbox']").click() # Click the consent checkbox
        time.sleep(1)
        driver.find_element(By.XPATH, "//span[text()='Next']").click() # Click the "Next" button
        time.sleep(2)

        # Section 2: Demographics
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(str(random.randint(18, 25)))  # Age
        gender = random.choice(genders)
        driver.find_element(By.XPATH, f"//div[@data-value='{gender}']").click() # Select a gender
        time.sleep(1)
        driver.find_element(By.XPATH, "//span[text()='Next']").click() # Click the "Next" button
        time.sleep(2)

        # Section 3: Currency & Spending
        currency = random.choice(currencies)
        driver.find_element(By.XPATH, f"//div[@data-value='{currency}']").click() # Select a currency
        time.sleep(1)
        short_answers = driver.find_elements(By.XPATH, "//input[@type='text']") # Get all short answer inputs
        short_answers[1].send_keys(random.choice(spending_estimates[currency])) # Fill the spending estimate
        time.sleep(1)
        driver.find_element(By.XPATH, "//span[text()='Next']").click() # Click the "Next" button
        time.sleep(2)

        # Section 4: Satisfaction
        driver.find_element(By.XPATH, f"//div[@data-value='{random.choice(satisfaction_levels)}']").click() # Select a satisfaction level
        time.sleep(1)

        # END OF FORM FILLING

        driver.find_element(By.XPATH, "//span[text()='Submit']").click() # Click the "Submit" button
        time.sleep(2)

        # Click "Submit another response" (if available)
        another = driver.find_element(By.XPATH, "//a[contains(text(),'Submit another response')]") # Find the "Submit another response" link
        another.click()
        time.sleep(2)

# End the infinite loop
except KeyboardInterrupt:
    print("Stopped by user.")
    driver.quit()