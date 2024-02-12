import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob

# Set download paths
download_path = "/home/Desktop/icici/iciciDownloads"
read_path = "/home/desktop/icici/*.csv"
chrome_driver = "/home/joelj/bane/ChromeDriver/chromedriver"

# Read CSV data
df = pd.concat([pd.read_csv(file) for file in glob.glob(read_path)])

# Configure Chrome options
options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": download_path
}
options.add_argument("--incognito")
options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
service = Service(chrome_driver)
driver = webdriver.Chrome(executable_path=chrome_driver, options=options)

# Loop through each row in DataFrame
for index, row in df.iterrows():
    # Navigate to the web page
    driver.get("https://ilhc.icicilombard.com/Customer/iCard")

    # Enter card number and age
    driver.find_element(By.ID, "NonRetail").click()
    driver.find_element(By.NAME, "CardNumber_CORPORATE").send_keys(str(row['CARD NUMBER']))
    driver.find_element(By.NAME, "AGE").send_keys(str(row['AGE']))
    driver.find_element(By.ID, "searchbtn").click()

    # Download PDF
    driver.find_element(By.ID, "SaveasPDF").click()

    # Wait for download to complete
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".downloaded")))

# Close WebDriver
driver.quit()
