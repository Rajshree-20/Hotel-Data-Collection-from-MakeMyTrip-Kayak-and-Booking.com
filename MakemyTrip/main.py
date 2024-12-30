from selenium import webdriver
from selenium.webdriver.chrome.service import Service #manages browser driver
from selenium.webdriver.common.by import By #locates elements on the webpage
from selenium.webdriver.chrome.options import Options  #configure browser setting
from selenium.webdriver.common.keys import Keys  #simulates keyboard input
from bs4 import BeautifulSoup
import time
import pandas as pd

url='https://www.makemytrip.com/hotels/hotel-listing/?checkin=01302025&city=CTBBI&checkout=01312025&roomStayQualifier=2e0e&locusId=CTBBI&country=IN&locusType=city&searchText=Bhubaneshwar&regionNearByExp=3&rsc=1e2e0e'
# Set up Selenium options
options = Options()
options.headless = True

chrome_driver_path = "C:\\Users\\rajsh\Downloads\\chromedriver-win64\\chromedriver.exe"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

time.sleep(5)

# Function to scroll and load more content
def scroll_and_load():
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(8):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

# Scroll and load all the content until no more content is loaded
previous_height = driver.execute_script("return document.body.scrollHeight")
while True:
    scroll_and_load()
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == previous_height:
        break
    previous_height = new_height

soup = BeautifulSoup(driver.page_source, 'html.parser')

hotellist = []

hotels = soup.find_all('div', {"class": "listingRowOuter hotelTileDt makeRelative"})
for bbs in hotels:
    try:
        name = bbs.find('span', {'class': 'wordBreak appendRight10'}).text
    except:
        name = 'N/A'
    try:
        location = bbs.find('span', {'class': 'blueText'}).text.strip()
    except:
        location = 'N/A'
    try:
        distance = bbs.find('span', {'class': 'latoRegular'}).text
    except:
        distance = 'N/A'
    try:
        rating_el = bbs.find("span", {"class": "ratingText latoBlack appendLeft3 darkBlueText font16"}).text.strip()
    except:
        rating_el = 'N/A'
    try:
        rating_score = bbs.find("span", {"class": "latoBlack blueBg ratingWrapper font14 appendLeft8 rating"}).text
    except:
        rating_score = 'N/A'
    try:
        review_count = bbs.find("p", {"class": "font14 darkGreyText appendTop5"}).text
    except:
        review_count = 'N/A'
    try:
        price = bbs.find("p", {"class": "priceText latoBlack font22 blackText appendBottom5"}).text.strip()
    except:
        price = 'N/A'
    try:
        tax_fee = bbs.find("p", {"class": "font14 midGreyText"}).text
    except:
        tax_fee = 'N/A'
    perks_set = set()
    try:
        perks = bbs.find_all('div', {'class': 'persuasion pc__inclusionsList'})
        for li in perks:
            Perks = li.text.strip()
            if Perks:
                perks_set.add(Perks)
    except:
        perks_set = set()
    Perks_Offered = ', '.join(perks_set)
    # Extract hotel link
    try:
        hotel_link = bbs.find('a', href=True)['href']
        hotel_link = 'https:'+hotel_link
    except:
        hotel_link = 'N/A'

    hotellist.append({
        "Name": name,
        "Location": location,
        "distance": distance,
        "review": rating_el,
        "review_score": rating_score,
        "review_count": review_count,
        "Offered Perk": Perks_Offered,
        "price": price,
        "tax-fee": tax_fee,
        "Hotel Link": hotel_link
    })

driver.quit()

df = pd.DataFrame(hotellist)
df.to_excel("MAKEMYTRIP_INFINTESCROLL", index=False) #file generated here use it as input for all other code in the folder that takes file as an input
print("Done!!")