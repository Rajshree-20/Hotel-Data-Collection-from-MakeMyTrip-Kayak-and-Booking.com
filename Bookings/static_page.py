import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
hotellist = []

url="https://www.booking.com/searchresults.en-gb.html?ss=Bhubaneshwar&ssne=Bhubaneshwar&ssne_untouched=Bhubaneshwar&efdco=1&label=bhubaneshwar-dvsCw9AYFUW*gyPni6aQDgS553381707338%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-355826131127%3Alp1007799%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfpWGnRw6lOGgfEoJVv7zYo&aid=1610687&lang=en-gb&sb=1&src_elem=sb&src=city&dest_id=-2091695&dest_type=city&checkin=2025-01-30&checkout=2025-01-31&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&sb_lp=1"
req = requests.get(url, headers= headers)

soup = BeautifulSoup(req.text, 'html.parser')

hotels = soup.find_all('div', {"class": "c1edfbabcb"})
for bbs in hotels:
    room= {
        'name' : bbs.find('h3', {'class':'aab71f8e4e'}).text,
    }
    hotellist.append(room)
    

df = pd.DataFrame(hotellist)
df.to_excel("STATIC_PAGE(BOOKINGS.COM).xlsx")
print("Done!!")
