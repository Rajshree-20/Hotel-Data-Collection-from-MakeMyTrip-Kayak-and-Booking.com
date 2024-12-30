from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Define the URL
url ='https://www.booking.com/searchresults.en-gb.html?ss=Bhubaneshwar&ssne=Bhubaneshwar&ssne_untouched=Bhubaneshwar&efdco=1&label=bhubaneshwar-dvsCw9AYFUW*gyPni6aQDgS553381707338%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-355826131127%3Alp1007799%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfpWGnRw6lOGgfEoJVv7zYo&aid=1610687&lang=en-gb&sb=1&src_elem=sb&src=city&dest_id=-2091695&dest_type=city&checkin=2025-01-30&checkout=2025-01-31&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&sb_lp=1'
# Set up Selenium options
options = Options()
options.headless = True  # Run the browser in headless mode

# Define the path to your ChromeDriver executable
chrome_driver_path = "C:\\Users\\rajsh\Downloads\\chromedriver-win64\\chromedriver.exe"

# Create a new instance of the Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load
    time.sleep(10)

    #virtualscroll with loadmore button
    old_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            # Scroll to the bottom of the page to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust sleep time as necessary

            # Check for the "Load More" button and click if available
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#bodyconstraint-inner > div:nth-child(8) > div > div.af5895d4b2 > div.df7e6ba27d > div.bcbf33c5c3 > div.dcf496a7b9.bb2746aad9 > div.d4924c9e74 > div.c82435a4b8.f581fde0b8 > button"))
                )
                load_more_button.click()
                time.sleep(2)  # Wait for new content to load
                print("Clicked 'Load More' button.")
            except Exception as e:
                print("No 'Load More' button found or clickable.", e)
                break

            # Check if new content is still loading
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == old_height:
                print("No more content to load.")
                break
            old_height = new_height

        except Exception as e:
            print(f"Error occurred during scrolling/loading: {e}")
            break
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    hotellist = []

    hotels = soup.find_all('div', {"data-testid": "property-card"})
    for bbs in hotels:
        name = bbs.find('div', {'class': 'f6431b446c a15b38c233'}).text
        link = bbs.find('a', {'class': 'a78ca197d0'})['href']
        distance = bbs.find('span', {'data-testid': 'distance'}).text
        thumbnail = bbs.find("img", {"data-testid": "image"})['src']
        rating_el = bbs.find("div", {"data-testid": "review-score"})
        review= bbs.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'}).text if bbs.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'}) else 'N/A'
        nuOfReviews = bbs.find('div', {'class': 'abf093bdfe f45d8e4c32 d935416c47'}).text if bbs.find('div', {'class': 'abf093bdfe f45d8e4c32 d935416c47'}) else 'N/A'
        location = bbs.find('span', {'class': 'aee5343fdb def9bc142a'}).text if bbs.find('span', {'class': 'aee5343fdb def9bc142a'}) else 'N/A'

        if rating_el:
            rating_text = rating_el.text.strip()
            review_count = rating_text.split(" ")[1] if len(rating_text.split(" ")) > 1 else None
        else:
            rating = None
            review_count = None
        hotellist.append({
            "Name": name,
            "Link": link,
            "DistanceFromCenter": distance,
            "Thumbnail": thumbnail,
            "Rating": review_count,
            "Review" : review,
            "NumberOfReview" : nuOfReviews,
            "Location" : location,
        })

finally:
    # Ensure the WebDriver quits after all operations are complete
    driver.quit()

# Create a dataframe from the list of dictionaries
df = pd.DataFrame(hotellist)

# Export the dataframe to an Excel file named 'result100.xlsx'
#df.to_excel('hotelAligarh.xlsx', index=False)
df.to_excel('2b.xlsx', index=False)

print("Data saved succesfully")