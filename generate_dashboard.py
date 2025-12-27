#!/usr/bin/env python3
import csv
import os
from datetime import datetime

def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Job Applications Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background: #2c3e50; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f9f9f9; }
        a { color: #3498db; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
        .status { padding: 4px 8px; border-radius: 4px; font-size: 12px; cursor: pointer; }
        .submitted { background: #2ecc71; color: white; }
        .failed { background: #e74c3c; color: white; }
        .generated { background: #f39c12; color: white; }
        .partial { background: #9b59b6; color: white; }
        .already_applied { background: #95a5a6; color: white; }
        .rejected { background: #34495e; color: white; }
        .stats { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        select { padding: 4px 8px; border-radius: 4px; border: 1px solid #ddd; }
    </style>
    <script>
        function updateStatus(url, newStatus) {
            fetch('/update_status', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url, status: newStatus})
            }).then(() => location.reload());
        }
        
        function deleteAll() {
            fetch('/delete_all', {method: 'POST'})
            .then(() => location.reload());
        }
        
        function removeDuplicates() {
            fetch('/remove_duplicates', {method: 'POST'})
            .then(() => location.reload());
        }
    </script>
</head>
<body>
    <h1>🎯 Job Applications Dashboard</h1>
    <div style="margin-bottom: 20px;">
        <button onclick="if(confirm('Delete all applications and start fresh?')) deleteAll()" style="background: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">🗑️ Clear All</button>
        <button onclick="if(confirm('Remove duplicate job URLs?')) removeDuplicates()" style="background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-left: 10px;">🧹 Remove Duplicates</button>
    </div>
    <div class="stats">
        <strong>Total Applications:</strong> {total} | 
        <strong>Submitted:</strong> {submitted} | 
        <strong>Generated:</strong> {generated} | 
        <strong>Failed:</strong> {failed}
    </div>
    <table>
        <tr>
            <th>Date</th>
            <th>Job Title</th>
            <th>Company</th>
            <th>Cover Letter</th>
            <th>Resume</th>
            <th>Status</th>
        </tr>
"""
    
    # Read CSV
    rows = []
    stats = {'total': 0, 'submitted': 0, 'generated': 0, 'failed': 0, 'partial': 0, 'already_applied': 0, 'rejected': 0}
    
    if os.path.exists('applications.csv'):
        with open('applications.csv', 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            stats['total'] = len(rows)
            for row in rows:
                status = row.get('status', 'unknown')
                if status in stats:
                    stats[status] += 1
    
    # Generate rows
    for row in reversed(rows):  # Most recent first
        timestamp = row['timestamp'][:19].replace('T', ' ')
        title = row['title']
        company = row['company']
        url = row['url']
        status = row['status']
        
        # Find cover letter file
        safe_name = f"{company}_{title}".replace('/', '_').replace(' ', '_')[:50]
        cover_files = [f for f in os.listdir('cover_letters') if f.startswith(safe_name)] if os.path.exists('cover_letters') else []
        cover_link = f'<a href="cover_letters/{cover_files[0]}" target="_blank">📄 View</a>' if cover_files else '—'
        
        # Resume link (placeholder - you can customize per job)
        resume_link = '<a href="resume.pdf" target="_blank">📋 View</a>'
        
        # Status dropdown
        statuses = ['submitted', 'partial', 'failed', 'generated', 'already_applied', 'rejected']
        status_options = ''.join([f'<option value="{s}" {"selected" if s == status else ""}>{s}</option>' for s in statuses])
        status_dropdown = f'<select onchange="updateStatus(\'{url}\', this.value)">{status_options}</select>'
        
        html += f"""
        <tr>
            <td>{timestamp}</td>
            <td><strong><a href="{url}" target="_blank">{title}</a></strong></td>
            <td>{company}</td>
            <td>{cover_link}</td>
            <td>{resume_link}</td>
            <td>{status_dropdown}</td>
        </tr>
"""
    
    html += """
    </table>
</body>
</html>
"""
    
    # Write HTML
    html = html.replace('{total}', str(stats['total']))
    html = html.replace('{submitted}', str(stats['submitted']))
    html = html.replace('{generated}', str(stats['generated']))
    html = html.replace('{failed}', str(stats['failed']))
    
    with open('dashboard.html', 'w') as f:
        f.write(html)
    
    print("✓ Dashboard generated: dashboard.html")
    print(f"  Total applications: {stats['total']}")

if __name__ == '__main__':
    generate_html()
