from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

url = 'https://www.kayak.co.in/hotels/Bhubaneswar,Odisha,India-p15995/2025-01-30/2025-01-31/2adults;map?ucs=1ja45o1&sort=rank_a'

# Set up Selenium options
options = Options()
options.headless = True 

chrome_driver_path = "C:\\Users\\rajsh\Downloads\\chromedriver-win64\\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

hotellist = []

# Function to scrape a single page
def scrape_page():
    time.sleep(2)  # Let the page load
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(35):  
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hotels = soup.find_all('div', {"class": "IirT"})
    
    for bbs in hotels:
        name = bbs.find('h3', {'class':'IirT-header'}).text
        thumbnail = bbs.find("img", {"class": "e9fk-photo"})['src']
        reviewcount = bbs.find("span", {"class": "IirT-rating-count"}).text if bbs.find("span", {"class": "IirT-rating-count"}) else 'N/A'
        rating = bbs.find("span", {"class": "IirT-rating-category"}).text if bbs.find("span", {"class": "IirT-rating-category"}) else 'N/A'
        price = bbs.find("div", {"class": "D8J--price-container"}).text.strip()

        hotellist.append({
            "Name": name,
            "Thumbnail": thumbnail,
            "reviewcount": reviewcount,
            "rating": rating,
            "price": price,
        })

# Open the initial URL
driver.get(url)
time.sleep(3)  # Initial wait for the page to load

# Loop through all pages
for page in range(1, 12):  # Adjust the range as needed
    scrape_page()
    
    if page < 11:  # Avoid clicking "Next" on the last page
        try:
            next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next page"]')
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # Adjust the sleep time if necessary to ensure the page loads completely
        except Exception as e:
            print(f"Failed to find or click 'Next' button on page {page}: {e}")
            break

driver.quit()

# Save the data to an Excel file
df = pd.DataFrame(hotellist)
df.to_excel("KAYAK_PAGINATION.xlsx", index=False)  #use this file that is generated here for all sub code that takes input as files
print("Done!!")