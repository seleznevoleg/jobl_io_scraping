import requests
import logging

def get_job_postings(company_id, token):
    """Fetch job postings for a specific company and return a list of dictionaries."""
    base_url = f"https://stats.k8s.jobl.io/v1/company_publication_info/{company_id}"
    
    # Set headers with authorization token
    headers = {
        'accept': '*/*',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'origin': 'https://www.jobl.io',
        'pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    
    try:
        # Make the request
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {})
            job_postings = []
            
            # Extract job postings
            for posting in data.get('attributes', {}).get('job_postings', []):
                job_postings.append({
                    'job_posting_id': posting.get('job_posting_id'),
                    'title': posting.get('title'),
                    'active_on_domains_count': len(posting.get('active_on_domains', []))
                })
            
            logging.info(f"Retrieved {len(job_postings)} job postings for company ID: {company_id}")
            return job_postings
        else:
            logging.error(f"Failed to fetch job postings, status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None
