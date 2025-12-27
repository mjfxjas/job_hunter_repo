# Job Hunter - Automated Application System

Automated job application bot that scrapes LinkedIn, generates tailored cover letters with Claude, and submits applications.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your credentials to `.env`:
- Get Anthropic API key: https://console.anthropic.com/
- Add LinkedIn credentials

4. Update `profile.py` with your info

## Run

```bash
python main.py
```

Applies to 50 jobs/day. Results logged to `applications.csv`.

## What It Does

1. Logs into LinkedIn
2. Searches for roles matching your profile
3. For each job:
   - Reads job description
   - Generates tailored cover letter with Claude
   - Fills Easy Apply form
   - Submits application
   - Logs to CSV

## Target Roles

Cloud Engineer, DevOps, Solutions Architect, TAM, Sales Engineer, HubSpot/Integration roles - anything tech >$50k
