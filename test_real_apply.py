#!/usr/bin/env python3
"""Test real application to 1 job"""
import os
from dotenv import load_dotenv
from scraper import JobScraper
from cover_letter import CoverLetterGenerator
from applicator import JobApplicator
from logger import ApplicationLogger

load_dotenv()

scraper = JobScraper(
    os.getenv('LINKEDIN_EMAIL'),
    os.getenv('LINKEDIN_PASSWORD')
)
generator = CoverLetterGenerator(os.getenv('ANTHROPIC_API_KEY'))
applicator = JobApplicator(scraper.driver)
logger = ApplicationLogger()

try:
    print("Logging into LinkedIn...")
    scraper.login_linkedin()
    print("✓ Logged in\n")
    
    print("Finding 1 job to apply to...")
    jobs = scraper.search_jobs(limit=1)
    
    if not jobs:
        print("No jobs found!")
        exit(1)
    
    job = jobs[0]
    
    print(f"\n{'='*60}")
    print(f"JOB: {job['title']}")
    print(f"COMPANY: {job['company']}")
    print(f"URL: {job['url']}")
    print(f"{'='*60}\n")
    
    # Check if already applied
    if logger.already_applied(job['url']):
        print("⏭️  Already applied to this job. Skipping.")
        exit(0)
    
    # Generate cover letter
    print("📝 Generating cover letter...\n")
    cover_letter = generator.generate(job)
    
    # Save it
    cover_file = logger.save_cover_letter(job, cover_letter)
    print(f"💾 Saved to: {cover_file}\n")
    
    # Show full cover letter
    print("="*60)
    print("COVER LETTER:")
    print("="*60)
    print(cover_letter)
    print("="*60)
    
    # Apply
    print("\n🚀 Submitting application...")
    success = applicator.apply_easy_apply(job, cover_letter)
    
    # Log
    status = 'submitted' if success else 'failed'
    logger.log(job, status)
    
    if success:
        print(f"\n✅ SUCCESS! Application submitted to {job['company']}")
    else:
        print(f"\n❌ FAILED. Could not submit application.")
    
    print(f"\nLogged to applications.csv")
    
finally:
    input("\nPress Enter to close browser...")
    scraper.close()
