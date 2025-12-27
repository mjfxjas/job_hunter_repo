#!/usr/bin/env python3
"""
Manual job application - paste job details and generate cover letter
"""
import os
from dotenv import load_dotenv
from cover_letter import CoverLetterGenerator
from logger import ApplicationLogger

def main():
    load_dotenv()
    
    print("=== Manual Job Application ===\n")
    
    # Get job details
    title = input("Job Title: ")
    company = input("Company: ")
    url = input("Job URL: ")
    print("\nPaste job description (press Ctrl+D when done):")
    
    description_lines = []
    try:
        while True:
            line = input()
            description_lines.append(line)
    except EOFError:
        pass
    
    description = '\n'.join(description_lines)
    
    job = {
        'title': title,
        'company': company,
        'url': url,
        'description': description,
        'source': 'Manual'
    }
    
    # Generate cover letter
    print("\n\nGenerating cover letter...")
    generator = CoverLetterGenerator(os.getenv('ANTHROPIC_API_KEY'))
    cover_letter = generator.generate(job)
    
    print("\n" + "="*60)
    print("COVER LETTER")
    print("="*60)
    print(cover_letter)
    print("="*60)
    
    # Log it
    logger = ApplicationLogger()
    logger.log(job, 'generated')
    
    print("\n✓ Logged to applications.csv")
    print("\nCopy the cover letter above and paste into your application!")

if __name__ == '__main__':
    main()
