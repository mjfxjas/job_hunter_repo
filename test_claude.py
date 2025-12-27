#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from cover_letter import CoverLetterGenerator

load_dotenv()

# Test Claude with a fake job
fake_job = {
    'title': 'Cloud Engineer',
    'company': 'AWS',
    'description': 'Looking for a Cloud Engineer with AWS experience to build scalable infrastructure. Must have experience with EC2, S3, Lambda, and Terraform.',
    'url': 'https://example.com',
    'source': 'Test'
}

print("Testing Claude cover letter generation...")
generator = CoverLetterGenerator(os.getenv('ANTHROPIC_API_KEY'))
cover_letter = generator.generate(fake_job)

print("\n✓ Cover letter generated:\n")
print(cover_letter)
print("\n✓ Claude API works!")
