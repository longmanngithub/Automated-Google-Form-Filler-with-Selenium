# 🤖 Automated Google Form Filler with Selenium

This Python script automates submissions to a Google Form using the Selenium library. It runs in headless mode for weightless operation, fills in randomized answers, and repeats the process at scheduled intervals during defined hours (e.g., 8 AM – 10 PM). Ideal for testing forms or learning how browser automation works. 

## 💡 FYI

This script was meant to offload into a server that runs indefinitely. Not to say it cannot run in a local machine, but it was meant for situation that you want to spam respond to your Google Form survey, this script can do just that.

> This script has been tested **24/7** on a Raspberry Pi 4 with Debian/Raspberry Pi OS (should also work for Pi 5). For the best result, modify the code to run on your prefered OS.


## 📦 Features

- ✅ Headless browser automation
- 🕒 Scheduled execution during active hours
- 🔁 Repeated submissions with random data
- 📄 Logging output to `log.txt`
- ⚙️ Auto-start on system boot (via cron)
- 🧪 Tested on Raspberry Pi with Chromium

## 🧰 Requirements

- Python 3.7+
- Chromium or Google Chrome
- ChromeDriver (matching your browser version)
- Selenium

### Install Selenium and Driver (Debian/Raspberry Pi OS)

```bash
sudo apt update
sudo apt install -y chromium-browser chromium-driver python3-selenium
```

Test the setup:

```bash
chromedriver --version
```

## 🚀 How to Use

1.	Clone or download this repository.
2.	Edit the form_url in automated_form_filler.py to match your Google Form.
3.	Make the script executable:

```bash
chmod +x automated_form_filler.py
```

4.	Run the script:

```bash
python3 automated_form_filler.py
```

> If `chromedriver` fails to run, make sure it’s located in `/usr/bin/` and matches your Chromium version.

## ⚙️ Auto-Start on Boot (Cron)

To run the script at boot and save output to a log file:

```bash
crontab -e
```

Add this line:

```bash
@reboot python3 /your-directory-path/automated_form_filler.py > /your-director-path/log.txt 2>&1 &
```

> [!NOTE]
> 
> Sometimes, it might use different `python3` (if you have multiple python versions installed). To check, simply just use the command `which python3` in your terminal to verify which version of python it is using.
> 
> For e.g., if `which python3` shows `/usr/bin/python3`, replace:
> ```bash
> @reboot python3 ...
> ```
> with
> ```bash
> @reboot /usr/bin/python3 ...
> ```

Ensure the log file exists and is writable:

```bash
touch /your-directory-path/log.txt
sudo chmod 755 /your-directory-path/log.txt
```

Reboot your device and check:

```bash
cat /your-directory-path/log.txt
```

## 🧠 How It Works

The script uses [Selenium WebDriver](https://www.selenium.dev/documentation/) to automate the browser:

### 📌 Selenium Functions Used

| Function | Purpose |
| --- | --- |
| `webdriver.Chrome()` | Initializes a Chrome browser instance with specified options (e.g., headless). |
| `driver.get(url)` | Opens the target URL (Google Form). |
| `driver.find_element(By.XPATH, ...)` | Finds a single element on the page using XPath. |
| `driver.find_elements(By.XPATH, ...)` | Finds multiple elements matching an XPath (e.g., all text inputs). |
| `element.click()` | Simulates a mouse click on an element (checkbox, button, option). |
| `element.send_keys(value)` | Types the given value into an input field. |
| `WebDriverWait(...).until(EC.presence_of_element_located(...))` | Waits until a specific element appears before proceeding (ensures page has loaded). |
| `time.sleep(seconds)` | Adds a pause (usually to let animations/transitions complete). |
| `random.choice([...])` | Picks a random option (used to simulate different user inputs). |

This combination allows the script to:	
- Click through sections
- Input values
- Select dropdowns/radio buttons
- Submit the form and optionally start another submission

## 🛑 Disable Auto-Start

Remove or comment out the crontab entry:

```bash
crontab -e
# @reboot python3 /home/youruser/Desktop/automated_form_filler.py > /home/youruser/Desktop/log.txt 2>&1 &
```

## 📌 Notes

- Do not use this script for spamming or malicious purposes.
- Use it on your own forms or with permission for educational/testing use.
- Google may detect or block frequent automated submissions.

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♀️ Credits

Made with ❤️ to help others learn web automation using Python + Selenium.

