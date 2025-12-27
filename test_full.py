#!/usr/bin/env python3
"""Test full pipeline: scrape + generate cover letters (no submission)"""
import os
from dotenv import load_dotenv
from scraper import JobScraper
from cover_letter import CoverLetterGenerator
from logger import ApplicationLogger

load_dotenv()

scraper = JobScraper(
    os.getenv('LINKEDIN_EMAIL'),
    os.getenv('LINKEDIN_PASSWORD')
)
generator = CoverLetterGenerator(os.getenv('ANTHROPIC_API_KEY'))
logger = ApplicationLogger()

try:
    print("Logging in...")
    scraper.login_linkedin()
    
    print("Scraping 3 jobs...")
    jobs = scraper.search_jobs(limit=3)
    print(f"✓ Found {len(jobs)} jobs\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"\n{'='*60}")
        print(f"JOB {i}: {job['title']} at {job['company']}")
        print('='*60)
        
        print("\nGenerating cover letter...")
        cover_letter = generator.generate(job)
        
        print(cover_letter[:200] + "...")
        
        logger.log(job, 'test_run')
        print("\n✓ Logged to applications.csv")
    
    print(f"\n\n✓ Full pipeline works! Ready to run main.py for real applications.")
    
finally:
    scraper.close()
