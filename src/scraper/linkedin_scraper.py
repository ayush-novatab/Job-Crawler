import requests
from bs4 import BeautifulSoup
import time
import random
from config.config import Config

def scrape_linkedin_software_jobs():  # Kept original function name
    headers = {
        "User-Agent": Config.USER_AGENT,
        "Referer": "https://www.linkedin.com/jobs/"
    }
    
    jobs = []
    search_query = "software engineer"
    location_query = "India"  # Specifically targeting India
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    try:
        for page in range(0, 3):  # Scrape first 3 pages (75 jobs)
            params = {
                "keywords": search_query,
                "location": location_query,  # Added location parameter
                "start": page * 25,
                "position": 1,
                "pageNum": 0
            }
            
            response = requests.get(base_url, headers=headers, params=params)
            soup = BeautifulSoup(response.text, "html.parser")
            
            for job in soup.find_all("li"):
                title_elem = job.find("h3", class_="base-search-card__title")
                company_elem = job.find("h4", class_="base-search-card__subtitle")
                location_elem = job.find("span", class_="job-search-card__location")
                url_elem = job.find("a", class_="base-card__full-link")
                
                if all([title_elem, company_elem, location_elem, url_elem]):
                    # Filter to ensure location contains "India" or specific Indian cities
                    location_text = location_elem.text.strip()
                    if ("India" in location_text or 
                        any(city in location_text for city in [
                            "Bangalore", "Bengaluru", "Mumbai", "Delhi", 
                            "Hyderabad", "Chennai", "Pune", "Kolkata", 
                            "Noida", "Gurgaon", "Gurugram", "Ahmedabad"
                        ])):
                        jobs.append({
                            "title": title_elem.text.strip(),
                            "company": company_elem.text.strip(),
                            "location": location_text,
                            "url": url_elem["href"].split('?')[0],
                            "source": "LinkedIn"
                        })
            
            time.sleep(random.uniform(2, 4))  # Slightly longer random delay to avoid detection
        
        return jobs
    
    except Exception as e:
        print(f"LinkedIn Scraping Error: {str(e)}")
        return []

# For backward compatibility you could also add this alias
scrape_linkedin_software_jobs_india = scrape_linkedin_software_jobs