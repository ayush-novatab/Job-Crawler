import requests
from bs4 import BeautifulSoup
from config.config import Config

def scrape_indeed():
    headers = {"User-Agent": Config.USER_AGENT}
    url = "https://www.indeed.com/jobs?q=software+engineer"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    jobs = []
    for job in soup.select(".job_seen_beacon"):
        title = job.select_one(".jobTitle").text.strip()
        company = job.select_one(".companyName").text.strip()
        location = job.select_one(".companyLocation").text.strip()
        url = "https://indeed.com" + job.find("a")["href"]
        
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "url": url
        })
    return jobs