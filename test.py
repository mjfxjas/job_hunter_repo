#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from scraper import JobScraper
from cover_letter import CoverLetterGenerator

def test():
    load_dotenv()
    
    # Test 1: LinkedIn login
    print("Testing LinkedIn login...")
    scraper = JobScraper(
        os.getenv('LINKEDIN_EMAIL'),
        os.getenv('LINKEDIN_PASSWORD')
    )
    scraper.login_linkedin()
    print("✓ Login successful\n")
    
    # Test 2: Scrape 3 jobs
    print("Testing job scraper (3 jobs)...")
    jobs = scraper.search_jobs(limit=3)
    print(f"✓ Found {len(jobs)} jobs\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"Job {i}:")
        print(f"  Title: {job['title']}")
        print(f"  Company: {job['company']}")
        print(f"  URL: {job['url'][:50]}...")
        print()
    
    # Test 3: Generate cover letter
    print("Testing Claude cover letter generation...")
    generator = CoverLetterGenerator(os.getenv('ANTHROPIC_API_KEY'))
    cover_letter = generator.generate(jobs[0])
    print("✓ Cover letter generated:\n")
    print(cover_letter)
    print()
    
    scraper.close()
    print("\n✓ All tests passed! Ready to run main.py")

if __name__ == '__main__':
    test()
