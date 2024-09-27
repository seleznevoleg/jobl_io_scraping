import logging
from datetime import datetime

def setup_logging():
    """Set up logging to write to a file with the date and time in the filename."""
    log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Set up logging to write to a file
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Remove existing handlers to prevent logging to the console
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up a file handler
    file_handler = logging.FileHandler(log_filename)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    # If you want to add logging to the console as well, you can uncomment this:
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # logging.getLogger().addHandler(console_handler)
