import logging
import os

# Ensure logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure the logging
logging.basicConfig(
    filename="logs/pentest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    """
    Log an informational message to console and file
    """
    print(f"[INFO] {message}")
    logging.info(message)

def log_error(message):
    """
    Log an error message to console and file
    """
    print(f"[ERROR] {message}")
    logging.error(message)

