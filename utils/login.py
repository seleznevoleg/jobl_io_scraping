import gzip
import brotli
import logging
from seleniumwire import webdriver  # Use selenium-wire to intercept requests
from selenium.webdriver.common.by import By
import time
import zlib
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def decode_response(response_body, encoding):
    """Function to decompress the response body based on its encoding."""
    if encoding == 'gzip':
        return gzip.decompress(response_body).decode('utf-8', errors='ignore')
    elif encoding == 'deflate':
        return zlib.decompress(response_body, -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
    elif encoding == 'br':
        return brotli.decompress(response_body).decode('utf-8', errors='ignore')
    else:
        return response_body.decode('utf-8', errors='ignore')

def get_id_token(login, password):
    """Function to get id_token using login and password."""
    link = "https://www.jobl.io"
    
    # Initialize WebDriver with selenium-wire to intercept requests
    browser = webdriver.Chrome()
    
    try:
        logging.info("Navigating to the login page.")
        # Navigate to the website
        browser.get(link)
        
        # Click the "Login with joblocal credentials" button
        login_button = browser.find_element(By.CSS_SELECTOR, "#app > div > div > div > form > a > span.MuiButton-label")
        login_button.click()

        # Find email and password fields
        email_field = browser.find_element(By.CSS_SELECTOR, "#inputEmail")
        password_field = browser.find_element(By.CSS_SELECTOR, "#inputPassword")
        
        # Find the submit button
        submit_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        logging.info("Entering login credentials.")
        # Enter email and password
        email_field.send_keys(login)
        password_field.send_keys(password)
        
        # Click the submit button
        submit_button.click()

        # Increase wait time to allow all requests to complete
        logging.info("Waiting for the login request to complete.")
        time.sleep(10)

        # Iterate through all requests and check for the request to 'https://auth.joblocal.de/oauth2/token'
        for request in browser.requests:
            if 'https://auth.joblocal.de/oauth2/token' in request.url and request.method == 'POST':
                # Get the response encoding type
                encoding = request.response.headers.get('Content-Encoding', '')
                
                # Decode the response body based on the encoding
                decoded_body = decode_response(request.response.body, encoding)
                
                # Convert the response body to JSON
                response_data = json.loads(decoded_body)
                
                # Extract and return the id_token
                id_token = response_data.get('id_token')
                logging.info(f"id_token successfully retrieved: {id_token}")
                return id_token

    except Exception as e:
        logging.error(f"An error occurred while processing: {e}")

    finally:
        logging.info("Closing the browser.")
        time.sleep(2)
        browser.quit()

    logging.warning("id_token not found or request failed.")
    return None  # Return None if the request is not found or failed
