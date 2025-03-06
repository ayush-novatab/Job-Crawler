import requests
from bs4 import BeautifulSoup
import time
import random
from config.config import Config
import logging

def scrape_glassdoor_software_jobs():
    logging.info("Starting Glassdoor scraper for India-based software jobs...")
    
    headers = {
        "User-Agent": Config.USER_AGENT,
        "Referer": "https://www.glassdoor.com/Job/"
    }
    
    jobs = []
    search_query = "software engineer"
    base_url = "https://www.glassdoor.com/Job/jobs.htm"
    
    try:
        params = {
            "sc.keyword": search_query,
            "locT": "N",         # National
            "locId": "115",      # India's location ID in Glassdoor
            "jobType": "all"
        }
        
        logging.info(f"Sending request to Glassdoor with params: {params}")
        response = requests.get(base_url, headers=headers, params=params)
        logging.info(f"Glassdoor response status: {response.status_code}")
        
        if response.status_code != 200:
            logging.warning(f"Glassdoor returned non-200 status code: {response.status_code}")
            logging.warning(f"Response content preview: {response.text[:200]}...")
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        logging.info(f"Parsed Glassdoor HTML response, searching for job listings...")
        
        # Log the first 500 characters for debugging
        logging.debug(f"HTML preview: {response.text[:500]}...")
        
        # Try to find job listings - first try the standard pattern
        job_listings = soup.find_all("li", class_="react-job-listing")
        
        # If standard pattern doesn't work, try alternative patterns
        if not job_listings:
            logging.info("No jobs found with primary selector, trying alternatives...")
            job_listings = soup.find_all("div", class_="jobCard") or soup.find_all("li", {"data-test": "jobListing"})
        
        logging.info(f"Found {len(job_listings)} potential job listings")
        
        for job in job_listings:
            try:
                # Extract job details with multiple selector attempts for robustness
                # Title extraction
                title_elem = (job.find("a", {"data-test": "job-link"}) or 
                              job.find("a", class_="jobTitle") or
                              job.find("div", class_="jobTitle"))
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                # Company extraction
                company_elem = (job.find("div", class_="d-flex justify-content-between align-items-start") or
                               job.find("div", class_="companyName") or
                               job.find("div", {"data-test": "employer-name"}))
                company = company_elem.text.strip() if company_elem else "Unknown Company"
                
                # Location extraction - try multiple classes
                location_elem = (job.find("span", class_="css-1buaf54") or 
                                job.find("span", {"data-test": "location"}) or
                                job.find("div", class_="location") or
                                job.find("span", class_="loc"))
                location = location_elem.text.strip() if location_elem else "Unknown Location"
                
                # URL extraction
                url_elem = job.find("a", class_="jobLink") or job.find("a", {"data-test": "job-link"})
                if url_elem and "href" in url_elem.attrs:
                    url = url_elem["href"]
                    if not url.startswith("http"):
                        url = "https://www.glassdoor.com" + url
                else:
                    url = ""
                
                # Verify it's an India-based job
                india_cities = ["Bangalore", "Bengaluru", "Mumbai", "Delhi", "Hyderabad", 
                                "Chennai", "Pune", "Kolkata", "Noida", "Gurgaon", 
                                "Gurugram", "Ahmedabad", "India"]
                
                is_india_job = any(city.lower() in location.lower() for city in india_cities)
                
                if is_india_job:
                    job_data = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "url": url,
                        "source": "Glassdoor"
                    }
                    logging.info(f"Found India job: {title} at {company} in {location}")
                    jobs.append(job_data)
                else:
                    logging.debug(f"Skipping non-India job: {title} at {company} in {location}")
            
            except Exception as e:
                logging.warning(f"Error parsing job listing: {str(e)}")
                continue
        
        logging.info(f"Successfully extracted {len(jobs)} India-based jobs from Glassdoor")
        # Add a random delay to avoid detection
        time.sleep(random.uniform(3, 6))
        return jobs
    
    except Exception as e:
        logging.error(f"Glassdoor Scraping Error: {str(e)}")
        return []

# For testing directly
if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    india_jobs = scrape_glassdoor_software_jobs()
    print(f"Found {len(india_jobs)} software engineering jobs in India on Glassdoor")
    for job in india_jobs[:5]:
        print(f"{job['title']} at {job['company']} ({job['location']})")