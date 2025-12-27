#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from scraper import JobScraper

load_dotenv()

print("Testing LinkedIn scraper...")
scraper = JobScraper(
    os.getenv('LINKEDIN_EMAIL'),
    os.getenv('LINKEDIN_PASSWORD')
)

try:
    scraper.login_linkedin()
    print("✓ Logged in\n")
    
    print("Scraping 5 jobs...")
    jobs = scraper.search_jobs(limit=5)
    
    print(f"\n✓ Found {len(jobs)} jobs:\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   URL: {job['url'][:60]}...")
        print(f"   Description: {job['description'][:100]}...")
        print()
    
    if len(jobs) > 0:
        print("✓ Scraper works!")
    else:
        print("✗ No jobs found - need to debug selectors")
        
finally:
    scraper.close()
