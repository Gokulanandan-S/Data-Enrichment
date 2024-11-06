from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

website_url = "https://www.cardiffmet.ac.uk/"
driver.get(website_url)

# Handle Cookiebot cookie consent pop-up by Usercentrics if it exists
try:
    allow_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All') or contains(text(), 'Allow all')]"))
    )
    allow_cookies_button.click()
    print("Cookie consent accepted.")
except Exception as e:
    print("No cookie consent popup found:", e)

# Find the search bar, enter the search query, and retrieve results
try:
    search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "search")))
    search_query = "Jack Talbot"
    search_bar.send_keys(search_query)
    search_bar.send_keys(Keys.RETURN)
    
    time.sleep(3)  # Wait for the search results to load

    # Extract and print URLs from the search results
    results = driver.find_elements(By.CSS_SELECTOR, "a")
    found_results = False
    for result in results:
        link = result.get_attribute("href")
        text = result.text  # Get visible text of the link
        if link and (search_query.lower() in link.lower() or search_query.lower() in text.lower()):
            print("Search result link:", link)
            found_results = True

    if not found_results:
        print("No matching results found for:", search_query)

except Exception as e:
    print("Search bar not found or search failed:", e)

driver.quit()
