import anthropic
from profile import PROFILE

class CoverLetterGenerator:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, job):
        prompt = f"""Write a concise, compelling cover letter for this job application.

Job Title: {job['title']}
Company: {job['company']}
Job Description: {job['description'][:1000]}

Candidate Profile:
- Name: {PROFILE['name']}
- Background: {PROFILE['summary']}
- Skills: {', '.join(PROFILE['skills'][:8])}
- Certifications: {', '.join(PROFILE['certifications'])}
- Recent Work: {PROFILE['recent_projects'][0]}

Write a 3-paragraph cover letter that:
1. Shows genuine interest and relevant experience
2. Highlights AWS/cloud skills and fast execution
3. Emphasizes hunger to break into tech from media background

Keep it under 250 words. Be authentic, not generic."""

        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
