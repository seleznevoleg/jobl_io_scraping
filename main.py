from utils.get_publication_stats import get_publication_stats
from utils.login import get_id_token
from utils.get_companies_ids import get_company_ids
from utils.get_job_postings import get_job_postings
from utils.logging_setup import setup_logging  # Import logging setup
import logging

# Set up logging
setup_logging()

# Login and password user inpout
login = input("Enter joblocal admin login: ")
password = input("Enter joblocal admin password: ")

# Get the id_token
id_token = get_id_token(login, password)

if id_token:
    logging.info(f"Successfully retrieved id_token: {id_token}")
    companies = get_company_ids()
    logging.info(f"Found {len(companies)} companies.")
    
    # User input for company ID
    while True:
        company_id = input("Please enter the company ID: ").strip()
        if company_id in companies:
            logging.info(f"Company found: {companies[company_id]} (ID: {company_id})")
            break
        else:
            logging.error("Invalid company ID, please try again.")

    # Fetch job postings and display result
    job_postings = get_job_postings(company_id, id_token)
    if job_postings:
        # for posting in job_postings:
        #     print(f"Job Posting ID: {posting['job_posting_id']}, Title: {posting['title']}, Active Domains Count: {posting['active_on_domains_count']}")
        
        # Extract job_posting_ids and fetch publication stats
        job_posting_ids = [posting['job_posting_id'] for posting in job_postings]
        get_publication_stats(job_posting_ids, id_token, company_id)
    else:
        logging.error("No job postings found for this company.")
else:
    logging.error("Failed to retrieve id_token")
