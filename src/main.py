import sys
import os

# Add this before any imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import your modules
from src.database.db_handler import init_db, save_job
from src.scraper.indeed_scraper import scrape_indeed
from src.scraper.linkedin_scraper import scrape_linkedin_software_jobs
from src.scraper.glassdoor_scraper import scrape_glassdoor_software_jobs
from src.email_sender.email_sender import send_email
import logging
import os
import traceback

# Create logs directory if missing
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/crawler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def main():
    logging.info("Job crawler starting...")
    init_db()
    
    # Track statistics for reporting
    all_jobs = []
    job_counts = {"LinkedIn": 0, "Glassdoor": 0, "Indeed": 0}
    
    try:
        # LinkedIn scraper
        logging.info("Starting LinkedIn scraper...")
        try:
            linkedin_jobs = scrape_linkedin_software_jobs()
            job_counts["LinkedIn"] = len(linkedin_jobs)
            logging.info(f"LinkedIn scraper found {len(linkedin_jobs)} jobs")
            all_jobs.extend(linkedin_jobs)
        except Exception as e:
            logging.error(f"LinkedIn scraper failed: {str(e)}")
            logging.error(traceback.format_exc())
        
        # Glassdoor scraper
        logging.info("Starting Glassdoor scraper...")
        try:
            glassdoor_jobs = scrape_glassdoor_software_jobs()
            job_counts["Glassdoor"] = len(glassdoor_jobs)
            logging.info(f"Glassdoor scraper found {len(glassdoor_jobs)} jobs")
            all_jobs.extend(glassdoor_jobs)
        except Exception as e:
            logging.error(f"Glassdoor scraper failed: {str(e)}")
            logging.error(traceback.format_exc())
        
        # Indeed scraper
        logging.info("Starting Indeed scraper...")
        try:
            indeed_jobs = scrape_indeed()
            job_counts["Indeed"] = len(indeed_jobs)
            logging.info(f"Indeed scraper found {len(indeed_jobs)} jobs")
            all_jobs.extend(indeed_jobs)
        except Exception as e:
            logging.error(f"Indeed scraper failed: {str(e)}")
            logging.error(traceback.format_exc())
        
        # Log summary of jobs found
        logging.info(f"Total jobs found: {len(all_jobs)} (LinkedIn: {job_counts['LinkedIn']}, Glassdoor: {job_counts['Glassdoor']}, Indeed: {job_counts['Indeed']})")
        
        # Save jobs and detect new ones
        new_jobs = []
        for job in all_jobs:
            try:
                is_new = save_job(job)
                if is_new:
                    new_jobs.append(job)
            except Exception as e:
                logging.error(f"Failed to save job: {e}")
        
        # Send alerts
        if new_jobs:
            logging.info(f"Found {len(new_jobs)} new jobs")
            try:
                send_email(new_jobs)
                logging.info(f"Sent email alert with {len(new_jobs)} new jobs from: {', '.join(set(j['source'] for j in new_jobs))}")
            except Exception as e:
                logging.error(f"Failed to send email: {str(e)}")
        else:
            logging.info("No new jobs found across all platforms")
            
    except Exception as e:
        logging.error(f"Critical error in main process: {str(e)}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()