import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_company_ids():
    """Function to retrieve the list of all company IDs and their names from the API."""
    # Base API URL
    base_url = "https://api.joblocal.de/v4/unified-search-companies/results"
    
    # Parameters for the first page request
    params = {
        'page.size': 100,  # Maximum number of items per page
        'page.number': 1,  # Start from the first page
        'fields.search-company': 'name',
        'search.query': 'a'
    }
    
    # Request headers
    headers = {
        'accept': 'application/json'
    }

    companies = {}

    try:
        # Make the first request to get the total number of pages
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response

            # Get the total number of pages
            total_pages = data['meta']['pagination']['total_pages']
            logging.info(f"Total pages: {total_pages}")

            # Extract companies from the first page
            for company in data.get('data', []):
                companies[company['id']] = company['attributes']['name']
            
            # Loop through all remaining pages
            for page in range(2, total_pages + 1):
                logging.info(f"Fetching page {page} of {total_pages}")
                
                # Update the page number parameter
                params['page.number'] = page
                
                # Make the request for the next page
                response = requests.get(base_url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract companies from this page
                    for company in data.get('data', []):
                        companies[company['id']] = company['attributes']['name']
                else:
                    logging.error(f"Error fetching page {page}: {response.status_code}")
                    break

            return companies
        else:
            logging.error(f"Error fetching the first page: {response.status_code}")
            return {}

    except requests.RequestException as e:
        logging.error(f"Request error occurred: {e}")
        return {}
