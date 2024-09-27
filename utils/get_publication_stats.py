import requests
import csv
import logging
from datetime import datetime

def get_publication_stats(job_posting_ids, token, company_id):
    """Fetch publication statistics for each job posting and write them to a CSV file."""
    base_url = "https://stats.k8s.jobl.io/v1/job_postings"
    
    # Set headers with authorization token
    headers = {
        'accept': '*/*',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'origin': 'https://www.jobl.io',
        'pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    # Generate the CSV filename dynamically based on the company ID and current date
    csv_filename = f"publication_stats_{company_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Open CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['job_posting_id', 'title', 'active_on_domains_count', 'publication_days',
                      'impressions', 'job_views', 'application_contact_information_requests',
                      'apply_button_clicks_with_redirect', 'applications', 'hr_tool']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for job_posting_id in job_posting_ids:
            # Updated URL with job_posting_id in the path
            url = f"{base_url}/{job_posting_id}?truncate=true"
            logging.info(f"Constructed URL for job posting: {url}")

            try:
                # Log request details
                logging.info(f"Fetching stats for job posting ID: {job_posting_id}")
                logging.info(f"Request URL: {url}")
                logging.info(f"Request Headers: {headers}")

                # Make the request for each job posting
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json().get('data', {})
                    attributes = data.get('attributes', {})
                    
                    # Extract relevant data
                    row = {
                        'job_posting_id': job_posting_id,
                        'title': attributes.get('title', 'N/A'),
                        'active_on_domains_count': len(attributes.get('active_on_domains', [])),
                        'publication_days': attributes.get('publication_days', {}).get('all,domain=all', 0),
                        'impressions': attributes.get('impressions', {}).get('all,domain=all', 0),
                        'job_views': attributes.get('job_views', {}).get('all,domain=all', 0),
                        'application_contact_information_requests': attributes.get('application_contact_information_requests', {}).get('all,domain=all', 0),
                        'apply_button_clicks_with_redirect': attributes.get('apply_button_clicks_with_redirect', {}).get('all,domain=all', 0),
                        'applications': attributes.get('applications', {}).get('all,domain=all', 0),
                        'hr_tool': attributes.get('hr_tool', False)
                    }

                    # Write the data to the CSV file
                    writer.writerow(row)
                    logging.info(f"Successfully wrote stats for job posting ID: {job_posting_id}")
                else:
                    logging.error(f"Failed to fetch stats for job posting ID: {job_posting_id}, status code: {response.status_code}")
                    logging.error(f"Response Body: {response.text}")  # Log the response body for debugging
            
            except requests.RequestException as e:
                logging.error(f"Request error for job posting ID {job_posting_id}: {e}")

            # Additional debug to check job_posting_id format
            logging.debug(f"Job posting ID used in the request: {job_posting_id}")
