import requests
from bs4 import BeautifulSoup
import time
import random
from config.config import Config

def scrape_glassdoor_software_jobs():
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
            "locT": "N",  # Nationwide (US)
            "jobType": "all"
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for job in soup.find_all("li", class_="react-job-listing"):
            title = job.find("a", {"data-test": "job-link"}).text.strip()
            company = job.find("div", class_="d-flex justify-content-between align-items-start").text.strip()
            location = job.find("span", class_="css-1buaf54").text.strip()
            url = "https://www.glassdoor.com" + job.find("a", class_="jobLink")["href"]
            
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "source": "Glassdoor"
            })
        
        time.sleep(random.randint(2, 5))
        return jobs
    
    except Exception as e:
        print(f"Glassdoor Scraping Error: {str(e)}")
        return []