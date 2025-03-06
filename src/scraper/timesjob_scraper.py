import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from config.config import Config

def scrape_timesjobs_software_jobs():
    logging.info("Starting TimesJobs scraper for India-based software jobs...")
    
    headers = {
        "User-Agent": Config.USER_AGENT,
        "Referer": "https://www.timesjobs.com/"
    }
    
    jobs = []
    url = "https://www.timesjobs.com/jobsearch/software-engineer-jobs"
    
    try:
        logging.info(f"Sending request to TimesJobs: {url}")
        response = requests.get(url, headers=headers)
        logging.info(f"TimesJobs response status: {response.status_code}")
        
        if response.status_code != 200:
            logging.warning(f"TimesJobs returned non-200 status code: {response.status_code}")
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find job listings
        job_listings = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        logging.info(f"Found {len(job_listings)} potential job listings")
        
        for job in job_listings:
            try:
                title_elem = job.find("h2")
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                company_elem = job.find("h3", class_="joblist-comp-name")
                company = company_elem.text.strip() if company_elem else "Unknown Company"
                
                location_elem = job.find("ul", class_="top-jd-dtl clearfix").find("li")
                location = location_elem.text.strip() if location_elem else "Unknown Location"
                
                url_elem = job.find("h2").find("a")
                url = url_elem["href"] if url_elem and "href" in url_elem.attrs else ""
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url,
                    "source": "TimesJobs"
                })
                logging.info(f"Added job: {title} at {company} in {location}")
                
            except Exception as e:
                logging.warning(f"Error parsing job listing: {str(e)}")
                continue
        
        logging.info(f"Successfully extracted {len(jobs)} jobs from TimesJobs")
        
    except Exception as e:
        logging.error(f"TimesJobs Scraping Error: {str(e)}")
    
    return jobs
