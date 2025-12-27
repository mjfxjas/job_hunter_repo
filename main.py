#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from scraper import JobScraper
from cover_letter import CoverLetterGenerator
from applicator import JobApplicator
from logger import ApplicationLogger

def main():
    load_dotenv()
    
    # Initialize
    scraper = JobScraper(
        os.getenv('LINKEDIN_EMAIL'),
        os.getenv('LINKEDIN_PASSWORD')
    )
    generator = CoverLetterGenerator(os.getenv('ANTHROPIC_API_KEY'))
    logger = ApplicationLogger()
    
    try:
        # Login
        print("Logging into LinkedIn...")
        scraper.login_linkedin()
        
        # Scrape jobs
        print("Scraping jobs...")
        jobs = scraper.search_jobs(limit=10)
        print(f"Found {len(jobs)} jobs")
        
        # Apply to each
        applicator = JobApplicator(scraper.driver)
        applied_count = 0
        skipped_count = 0
        
        for i, job in enumerate(jobs, 1):
            print(f"\n[{i}/{len(jobs)}] {job['title']} at {job['company']}")
            
            # Skip if already applied
            if logger.already_applied(job['url']):
                print("  ⏭️  Already applied - skipping")
                skipped_count += 1
                continue
            
            # Generate cover letter
            print("  📝 Generating cover letter...")
            cover_letter = generator.generate(job)
            
            # Save cover letter
            cover_file = logger.save_cover_letter(job, cover_letter)
            print(f"  💾 Saved to {cover_file}")
            
            # Show preview
            print(f"\n  {'-'*58}")
            print(f"  {cover_letter[:150]}...")
            print(f"  {'-'*58}\n")
            
            # Apply
            print("  🚀 Submitting application...")
            result = applicator.apply_easy_apply(job, cover_letter)
            
            # Log
            if result == 'already_applied':
                status = 'already_applied'
                logger.log(job, status)
                print(f"  ⏭️  Status: {status}")
                skipped_count += 1
            elif result == 'partial':
                status = 'partial'
                logger.log(job, status)
                print(f"  ⏸️  Status: {status} - finish manually")
            elif result:
                status = 'submitted'
                logger.log(job, status)
                print(f"  ✅ Status: {status}")
                applied_count += 1
            else:
                status = 'failed'
                logger.log(job, status)
                print(f"  ❌ Status: {status}")
        
        print(f"\n\n{'='*60}")
        print(f"✅ Applied: {applied_count}")
        print(f"⏭️  Skipped (already applied): {skipped_count}")
        print(f"📊 Total processed: {len(jobs)}")
        print(f"\nCover letters saved to: cover_letters/")
        print(f"Application log: applications.csv")
        print(f"{'='*60}")
        
        # Generate dashboard
        print("\n📊 Generating dashboard...")
        os.system('python generate_dashboard.py')
        print("\n🎉 Open dashboard.html in your browser to view all applications!")
        

        
    finally:
        scraper.close()

if __name__ == '__main__':
    main()
