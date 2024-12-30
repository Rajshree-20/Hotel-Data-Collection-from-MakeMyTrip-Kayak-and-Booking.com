import requests
from bs4 import BeautifulSoup
import pandas as pd

# User-Agent header to mimic a real browser request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

# Input file containing URLs
input_file = 'BOOKINGS_VIRTUALSCROLL.xlsx'
urls_df = pd.read_excel(input_file)

# Extract the URLs from the dataframe
urls = urls_df['Link'].tolist()

# List to hold amenities for each URL
amenities_list = []

for url in urls:
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(req.content, 'html.parser')
        
        # Find the section containing amenities
        amenities_section = soup.find_all('li', class_='d044972638 f8e733d28b ea41992eee ef88ed2ec6')
        amenities_set = set()
        
        # Extract the amenities and add them to the set
        for amenity in amenities_section:
            amenities_set.add(amenity.get_text(strip=True))
        
        # Convert the set to a comma-separated string and append to the list
        amenities = ', '.join(amenities_set)
        amenities_list.append(amenities)
    else:
        # If the request fails, append an empty string or some error message
        amenities_list.append('Request failed')

# Add the amenities list to the dataframe
urls_df['Amenities'] = amenities_list

# Save the dataframe back to an Excel file
output_file = 'BOOKINGS_AMENITIES.xlsx'
urls_df.to_excel(output_file, index=False)

print(f"Done!! Data saved to {output_file}")
