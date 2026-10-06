import csv
from datetime import datetime
import os

class ApplicationLogger:
    def __init__(self, filename='applications.csv'):
        self.filename = filename
        self.fieldnames = ['timestamp', 'title', 'company', 'url', 'status', 'source']
        
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def already_applied(self, job_url):
        """Check if we've already applied to this job"""
        if not os.path.exists(self.filename):
            return False
        
        with open(self.filename, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['url'] == job_url and row['status'] in ['submitted', 'generated', 'already_applied']:
                    return True
        return False
    
    def log(self, job, status):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'title': job['title'],
                'company': job['company'],
                'url': job['url'],
                'status': status,
                'source': job['source']
            })
    
    def save_cover_letter(self, job, cover_letter):
        """Save cover letter to file"""
        safe_name = f"{job['company']}_{job['title']}".replace('/', '_').replace(' ', '_')[:50]
        filename = f"cover_letters/{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        os.makedirs('cover_letters', exist_ok=True)
        
        with open(filename, 'w') as f:
            f.write(f"Job: {job['title']}\n")
            f.write(f"Company: {job['company']}\n")
            f.write(f"URL: {job['url']}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*60 + "\n\n")
            f.write(cover_letter)
        
        return filename
