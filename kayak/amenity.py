import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

input_file = 'KAYAK_PAGINATION.xlsx'
urls_df = pd.read_excel(input_file)

urls = urls_df['URL'].tolist()

amenities_list = []

for url in urls:
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    hotels = soup.find_all('div', {'class': 'JxVY-text-container'})
    
    # Use a set to avoid duplicates
    amenities_set = set()
    
    for bbs in hotels:
        li_elements = bbs.find_all('p', {'class': 'JxVY-text JxVY-line-clamp--4'})
        for li in li_elements:
            amenity = li.text.strip()
            if amenity:
                amenities_set.add(amenity)
    
    amenities = ', '.join(amenities_set)
    amenities_list.append(amenities)

urls_df['Comments'] = amenities_list

urls_df.to_excel(input_file, index=False)

print(f"Done!! Data saved")

