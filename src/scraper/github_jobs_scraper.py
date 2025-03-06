import requests
import logging
import time
from config.config import Config

def scrape_github_jobs():
    logging.info("Starting GitHub Jobs API scraper for India-based jobs...")
    
    jobs = []
    base_url = "https://jobs.github.com/positions.json"
    
    try:
        headers = {
            "User-Agent": Config.USER_AGENT
        }
        
        # Search for software engineering jobs in India
        params = {
            "description": "software engineer",
            "location": "India"
        }
        
        logging.info(f"Sending request to GitHub Jobs API with params: {params}")
        response = requests.get(base_url, headers=headers, params=params)
        logging.info(f"GitHub Jobs API response status: {response.status_code}")
        
        if response.status_code != 200:
            logging.warning(f"GitHub Jobs API returned non-200 status code: {response.status_code}")
            return jobs
        
        # Parse JSON response
        job_listings = response.json()
        logging.info(f"Found {len(job_listings)} potential job listings")
        
        for job in job_listings:
            try:
                jobs.append({
                    "title": job.get("title", "Unknown Title"),
                    "company": job.get("company", "Unknown Company"),
                    "location": job.get("location", "Unknown Location"),
                    "url": job.get("url", ""),
                    "source": "GitHub Jobs"
                })
                logging.info(f"Added job: {job.get('title')} at {job.get('company')} in {job.get('location')}")
                
            except Exception as e:
                logging.warning(f"Error parsing job listing: {str(e)}")
                continue
        
        logging.info(f"Successfully extracted {len(jobs)} India-based jobs from GitHub Jobs")
        
    except Exception as e:
        logging.error(f"GitHub Jobs API Scraping Error: {str(e)}")
    
    return jobs