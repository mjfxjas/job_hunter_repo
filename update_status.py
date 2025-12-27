#!/usr/bin/env python3
"""Simple server to handle status updates"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import csv
import os

class StatusHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/delete_all':
            # Clear CSV
            with open('applications.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'title', 'company', 'url', 'status', 'source'])
            
            # Clear cover letters
            if os.path.exists('cover_letters'):
                for f in os.listdir('cover_letters'):
                    os.remove(os.path.join('cover_letters', f))
            
            os.system('python generate_dashboard.py')
            self.send_response(200)
            self.end_headers()
        
        elif self.path == '/remove_duplicates':
            # Remove duplicate URLs, keep most recent
            rows = []
            seen_urls = set()
            
            with open('applications.csv', 'r') as f:
                reader = csv.DictReader(f)
                all_rows = list(reader)
            
            # Reverse to keep most recent
            for row in reversed(all_rows):
                if row['url'] not in seen_urls:
                    rows.insert(0, row)
                    seen_urls.add(row['url'])
            
            with open('applications.csv', 'w', newline='') as f:
                if rows:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
            
            os.system('python generate_dashboard.py')
            self.send_response(200)
            self.end_headers()
        
        elif self.path == '/update_status':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            url = data['url']
            new_status = data['status']
            
            # Update CSV
            rows = []
            with open('applications.csv', 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            for row in rows:
                if row['url'] == url:
                    row['status'] = new_status
            
            with open('applications.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            
            # Regenerate dashboard
            os.system('python generate_dashboard.py')
            
            self.send_response(200)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            with open('dashboard.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())

if __name__ == '__main__':
    print("Starting server on http://localhost:8000")
    print("Open http://localhost:8000 in your browser")
    server = HTTPServer(('localhost', 8000), StatusHandler)
    server.serve_forever()
