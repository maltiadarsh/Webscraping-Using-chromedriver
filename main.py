# Required Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Column mapping as specified
csv_cols = {
    "NIT/RFP NO": "ref_no",
    "Name of Work / Subwork / Packages": "title",
    "Estimated Cost": "tender_value",
    "Bid Submission Closing Date & Time": "bid_submission_end_date",
    "EMD Amount": "emd",
    "Bid Opening Date & Time": "bid_open_date"
}

# Set up Chrome driver
service = Service('chromedriver.exe') 
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

def scrape_current_page(driver):
    """Scrape tenders from the current page and return list of dicts."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_rows = soup.select('table#awardedDataTable tbody tr')[:10]  # top 10 rows

    records = []
    for row in table_rows:
        cells = row.find_all('td')
        if len(cells) >= 8:
            record = {
                "NIT/RFP NO": cells[1].get_text(strip=True),
                "Name of Work / Subwork / Packages": cells[2].get_text(strip=True),
                "Estimated Cost": cells[4].get_text(strip=True).replace('₹', '').replace(',', ''),
                "EMD Amount": cells[5].get_text(strip=True).replace('₹', '').replace(',', ''),
                "Bid Submission Closing Date & Time": cells[6].get_text(strip=True),
                "Bid Opening Date & Time": cells[7].get_text(strip=True)
            }
            records.append(record)
    return records

try:
    # Step 1: Open website
    driver.get('https://etender.cpwd.gov.in/') 
    wait.until(EC.element_to_be_clickable((By.ID, "viewCurrentall"))).click()
    time.sleep(3)

    # Step 2: Set dropdown to 20 rows
    select = Select(wait.until(EC.presence_of_element_located((By.NAME, "awardedDataTable_length"))))
    select.select_by_value("20")
    time.sleep(2)

    # Step 3: Scrape page 1
    all_data = scrape_current_page(driver)

    # Step 4: Click to page 2
    next_button = driver.find_element(By.CSS_SELECTOR, 'a#awardedDataTable_next')
    if "disabled" not in next_button.get_attribute("class"):
        next_button.click()
        time.sleep(3)
        all_data.extend(scrape_current_page(driver))

    # Step 5: Save to CSV
    df = pd.DataFrame(all_data)
    df.rename(columns=csv_cols, inplace=True)
    df.to_csv("tenders_top.csv", index=False)
    print("Data from page 1 and 2 saved to 'tenders_top.csv'")

finally:
    driver.quit()
