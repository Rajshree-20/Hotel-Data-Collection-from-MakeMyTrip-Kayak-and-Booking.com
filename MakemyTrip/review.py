from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Read the input Excel file
input_file = 'temp_aligarh.xlsx'
urls_df = pd.read_excel(input_file)

# List of URLs to scrape
urls = urls_df['Hotel Link'].tolist()

# List to store comments for each URL
all_comments = []

for url in urls:
    # Open the webpage
    driver.get(url)
    
    # Initialize a list to store comments for the current URL
    comments = []

    try:
        while True:
            # Wait for the comments section to be present
            comments_section = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.font14.lineHight20'))
            )

            # Extract the text of each comment
            for comment in comments_section:
                comments.append(comment.text)

            # Check if there is a next page button
            next_button = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="pagination"] a[aria-label="Next"]')
            if next_button:
                next_button[0].click()
                time.sleep(5)  # Wait for the next page to load
            else:
                break

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred for URL {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for URL {url}: {e}")
    
    # Append comments for the current URL to the main list
    all_comments.append(' | '.join(comments))

# Close the WebDriver
driver.quit()

# Add the scraped data to the DataFrame and save to Excel
urls_df['Comments'] = all_comments
urls_df.to_excel(input_file, index=False)

print("Done! Data saved.")
