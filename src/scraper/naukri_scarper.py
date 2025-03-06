import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from config.config import Config

def scrape_naukri_software_jobs():
    logging.info("Starting Naukri.com scraper for software engineering jobs...")
    
    headers = {
        "User-Agent": Config.USER_AGENT,
        "Referer": "https://www.naukri.com/"
    }
    
    jobs = []
    url = "https://www.naukri.com/software-engineer-jobs"
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        session.headers.update(headers)
        
        # First visit the homepage to get cookies
        session.get("https://www.naukri.com/")
        time.sleep(random.uniform(1, 3))
        
        # Then visit the job search page
        logging.info(f"Sending request to Naukri.com: {url}")
        response = session.get(url)
        logging.info(f"Naukri.com response status: {response.status_code}")
        
        if response.status_code != 200:
            logging.warning(f"Naukri.com returned non-200 status code: {response.status_code}")
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find job listings
        job_listings = soup.find_all("article", class_="jobTuple")
        logging.info(f"Found {len(job_listings)} potential job listings")
        
        for job in job_listings:
            try:
                title_elem = job.find("a", class_="title")
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                company_elem = job.find("a", class_="subTitle")
                company = company_elem.text.strip() if company_elem else "Unknown Company"
                
                location_elem = job.find("li", class_="location")
                location = location_elem.text.strip() if location_elem else "Unknown Location"
                
                url_elem = job.find("a", class_="title")
                url = url_elem["href"] if url_elem and "href" in url_elem.attrs else ""
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url,
                    "source": "Naukri"
                })
                logging.info(f"Added job: {title} at {company} in {location}")
                
            except Exception as e:
                logging.warning(f"Error parsing job listing: {str(e)}")
                continue
        
        logging.info(f"Successfully extracted {len(jobs)} jobs from Naukri.com")
        
    except Exception as e:
        logging.error(f"Naukri.com Scraping Error: {str(e)}")
    
    return jobs