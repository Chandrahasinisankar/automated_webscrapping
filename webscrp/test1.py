import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract
from PIL import Image
def take_fullpage_screenshot(url, filename='fullpage_screenshot.png', driver_path=None):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    
    # Set up Chrome service
    service = Service(driver_path)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open website
    driver.get(url)

    # Scroll to the bottom of the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Calculate dimensions of the page
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    
    # Take screenshot in segments
    screenshot = Image.new('RGB', (total_width, total_height))
    offset = 0
    while offset < total_height:
        driver.execute_script(f"window.scrollTo(0, {offset});")
        time.sleep(2)  # Adjust sleep time as needed
        screenshot_temp = driver.get_screenshot_as_png()
        screenshot_temp = Image.open(io.BytesIO(screenshot_temp))
        screenshot.paste(screenshot_temp, (0, offset))
        offset += screenshot_temp.size[1]

    # Save the final screenshot
    screenshot.save(filename)
    print(f"Screenshot of {url} saved as {filename}")

    # Close browser
    driver.quit()

def extract_text_from_screenshot(image_path):
    # Load the image
    img = Image.open(image_path)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(img)

    return text    

# Example usage:
driver_path = r"C:\Users\Chandrahasini Sankar\OneDrive\Desktop\chandrahasini\project\webscrp\chromedriver-win32\chromedriver.exe"
link = input("enter url : ")
take_fullpage_screenshot(link, 'fullpage_example_screenshot.png', driver_path)
screenshot_image_path = 'fullpage_example_screenshot.png'
extracted_text = extract_text_from_screenshot(screenshot_image_path)
print("Extracted Text:")
print(extracted_text)
