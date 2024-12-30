from selenium import webdriver
from selenium.webdriver.chrome.service import Service #manages browser driver
from selenium.webdriver.common.by import By #locates elements on the webpage
from selenium.webdriver.chrome.options import Options  #configure browser setting
from selenium.webdriver.common.keys import Keys  #simulates keyboard input
from bs4 import BeautifulSoup 
import time
import pandas as pd

url ='https://www.booking.com/searchresults.en-gb.html?ss=Bhubaneshwar&ssne=Bhubaneshwar&ssne_untouched=Bhubaneshwar&efdco=1&label=bhubaneshwar-dvsCw9AYFUW*gyPni6aQDgS553381707338%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-355826131127%3Alp1007799%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfpWGnRw6lOGgfEoJVv7zYo&aid=1610687&lang=en-gb&sb=1&src_elem=sb&src=city&dest_id=-2091695&dest_type=city&checkin=2025-01-30&checkout=2025-01-31&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&sb_lp=1'

# Set up Selenium options
options = Options()
options.headless = True 

chrome_driver_path = "C:\\Users\\rajsh\Downloads\\chromedriver-win64\\chromedriver.exe"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

time.sleep(2)

body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(40):  
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'html.parser')

hotellist = []

hotels = soup.find_all('div', {"data-testid": "property-card"})
for bbs in hotels:
    name = bbs.find('div', {'class':'f6431b446c a15b38c233'}).text
    link = bbs.find('a',{'class': 'a78ca197d0'})['href']
    location = bbs.find('span', {'data-testid': 'distance'}).text
    thumbnail = bbs.find("img", {"data-testid": "image"})['src']
    rating_el = bbs.find("div", {"data-testid": "review-score"})
    if rating_el:
        rating_text = rating_el.text.strip()
        rating = rating_text.split(" ")[0] if rating_text else None
        review_count = rating_text.split(" ")[1] if len(rating_text.split(" ")) > 1 else None
    else:
        rating = None
        review_count = None
    hotellist.append({
        "Name": name,
        "Link": link,
        "Location": location,
        "Thumbnail" : thumbnail,
        "rating": rating,
        "review_count": review_count,
    })
driver.quit()

df = pd.DataFrame(hotellist)
df.to_excel("BOOKINGS_VIRTUALSCROLL.xlsx")
print("Done!!")
