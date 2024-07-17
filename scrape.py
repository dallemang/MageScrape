import os
import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# Argument parsing
parser = argparse.ArgumentParser(description='Scrape images from a user profile.')
parser.add_argument('username', type=str, help='Username to scrape')
parser.add_argument('--scrolls', type=int, default=5, help='Number of page scrolls to do at the start (default: 5)')
parser.add_argument('--images', type=int, default=20, help='Number of new images to process (default: 20)')
args = parser.parse_args()

# Get the ChromeDriver path from the environment variable
chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
if not chromedriver_path:
    raise EnvironmentError('CHROMEDRIVER_PATH environment variable is not set')

# Create a Service object with the ChromeDriver path
service = Service(chromedriver_path)

# Create a new instance of the Chrome driver with the service object
options = webdriver.ChromeOptions()
options.add_argument("--disable-features=TranslateUI")
options.add_argument("--disable-extensions")
options.add_argument("--incognito")

driver = webdriver.Chrome(service=service, options=options)

# Navigate to the desired webpage
url = f'https://legacy.mage.space/u/{args.username}'
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Load previously processed original sources from a file
processed_file = 'processed_images.json'
main_images_file = 'main_images.json'

if os.path.exists(processed_file):
    with open(processed_file, 'r') as file:
        processed_images = set(json.load(file))
else:
    processed_images = set()

# Load previously processed main images from a file
if os.path.exists(main_images_file):
    with open(main_images_file, 'r') as file:
        main_images = json.load(file)
else:
    main_images = []

# Scroll down the webpage to load more content
for _ in range(args.scrolls):  # Adjust the range based on the command line argument
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Find all <img> elements with a non-empty 'alt' attribute
img_elements = [img for img in driver.find_elements(By.TAG_NAME, 'img') if img.get_attribute('alt')]

# Iterate over the found img elements, click on them, and process popups
new_processed_images = set()
new_main_images = []
for index in range(len(img_elements)):
    try:
        # Re-find the img elements to avoid stale element reference
        img_elements = [img for img in driver.find_elements(By.TAG_NAME, 'img') if img.get_attribute('alt')]
        img_element = img_elements[index]

        # Get the src of the original image
        original_src = img_element.get_attribute('src')

        # Skip if this image was processed in a previous run
        if original_src in processed_images:
            continue

        # Scroll the element into view and click on the image to open the popup
        driver.execute_script("arguments[0].scrollIntoView();", img_element)
        driver.execute_script("arguments[0].click();", img_element)

        time.sleep(3)  # Wait for the popup to load

        # Extract the main image's source from the popup
        try:
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'mantine-Modal-modal'))
            )
            main_image_element = popup.find_element(By.CSS_SELECTOR, '.mantine-gvt5r2.mantine-Image-image')
            main_image_src = main_image_element.get_attribute('src')
        except Exception as e:
            main_image_src = 'None'
            print(f"Error extracting main image: {e}")

        print(f"Original Image Src: {original_src}")
        print(f"Main Image Src: {main_image_src}")

        # Try to close the popup using the close button or by pressing the Escape key
        try:
            close_button = popup.find_element(By.CSS_SELECTOR, '.mantine-Modal-close')
            close_button.click()
        except Exception as e:
            print(f"Error closing popup with button: {e}")
            # Use JavaScript to press the Escape key to close the popup
            driver.execute_script("arguments[0].dispatchEvent(new KeyboardEvent('keydown', {'key': 'Escape'}));", popup)

        # Add the original source to the new processed images set
        new_processed_images.add(original_src)

        # Add the main image src to the new main images list
        new_main_images.append(main_image_src)

        # Add a short delay to prevent Chrome from thinking it's being interacted with too quickly
        time.sleep(1)

    except Exception as e:
        print(f"Error processing image at index {index}: {e}")

    # Break the loop after processing the specified number of new images
    if len(new_processed_images) >= args.images:
        break

# Update the processed images set
processed_images.update(new_processed_images)

# Save the processed images to the file
with open(processed_file, 'w') as file:
    json.dump(list(processed_images), file)

# Update the main images list
main_images.extend(new_main_images)

# Save the main images to the file
with open(main_images_file, 'w') as file:
    json.dump(main_images, file)

# Close the browser
driver.quit()
