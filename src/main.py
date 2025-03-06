import sys
import os

# Add this before any imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import your modules
# In main.py, change the imports to:
from src.database.db_handler import init_db, save_job
from src.scraper.indeed_scraper import scrape_indeed
from src.scraper.linkedin_scraper import scrape_linkedin_software_jobs
from src.scraper.glassdoor_scraper import scrape_glassdoor_software_jobs
from src.email_sender.email_sender import send_email
import logging
import os

# Create logs directory if missing
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/crawler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    init_db()
    try:
        # Scrape from all sources
        jobs = []
        jobs += scrape_linkedin_software_jobs()
        jobs += scrape_glassdoor_software_jobs()
        jobs += scrape_indeed()
        
        # Save jobs and detect new ones
        new_jobs = []
        for job in jobs:
            try:
                save_job(job)
                new_jobs.append(job)
            except Exception as e:
                logging.error(f"Failed to save job: {e}")
        
        # Send alerts
        if new_jobs:
            send_email(new_jobs)
            logging.info(f"Sent {len(new_jobs)} new jobs from: {', '.join(set(j['source'] for j in new_jobs))}")
        else:
            logging.info("No new jobs found across all platforms")
            
    except Exception as e:
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main()