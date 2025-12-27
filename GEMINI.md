# Gemini Code Companion Context

This document provides context for the "Job Hunter - Automated Application System" project to an AI code companion.

## Project Overview

This project is a Python-based automated job application bot. It scrapes job postings from LinkedIn, generates tailored cover letters using the Anthropic (Claude) API, and submits applications through LinkedIn's "Easy Apply" feature. The application's state and results are logged to a CSV file, and a simple HTML dashboard is generated to view the application history.

The core technologies used are:
- **Python:** The main programming language.
- **Selenium:** For web scraping and browser automation to interact with LinkedIn.
- **Anthropic API (Claude):** For generating tailored cover letters.
- **Dotenv:** For managing environment variables like API keys and login credentials.

The project is structured into several modules, each responsible for a specific part of the workflow: scraping, cover letter generation, application submission, and logging.

## File Descriptions

- **`main.py`:** The entry point of the application. It orchestrates the entire job application process, from logging in and scraping jobs to generating cover letters, applying, and logging the results.
- **`scraper.py`:** Contains the `JobScraper` class, which uses Selenium to log into LinkedIn, search for jobs based on predefined roles, and scrape job details.
- **`cover_letter.py`:** Contains the `CoverLetterGenerator` class, which uses the Anthropic API to generate a personalized cover letter for each job application based on the user's profile and the job description.
- **`applicator.py`:** Contains the `JobApplicator` class, which automates the application submission process on LinkedIn using the "Easy Apply" feature. It fills out forms, attaches the cover letter, and handles multi-step application processes.
- **`profile.py`:** A configuration file that stores the user's personal and professional information, such as name, contact details, work experience, skills, and job search preferences. This file is used by other modules to personalize the application process.
- **`logger.py`:**  Handles the logging of application statuses to `applications.csv` and saving generated cover letters.
- **`generate_dashboard.py`:** A script to generate an HTML dashboard from the `applications.csv` log file.
- **`requirements.txt`:** Lists the Python dependencies for the project.
- **`.env.example`:** An example file for setting up the `.env` file with the required environment variables.

## Building and Running

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create `.env` file:**
    Copy the `.env.example` file to `.env` and fill in your LinkedIn credentials and Anthropic API key.
    ```bash
    cp .env.example .env
    ```

3.  **Update your profile:**
    Edit the `profile.py` file to reflect your personal and professional information.

4.  **Run the application:**
    ```bash
    python main.py
    ```
    The bot will start applying to jobs, and the progress will be logged to `applications.csv`.

## Development Conventions

- The project follows a modular structure, with each file having a specific responsibility.
- It uses a central `profile.py` file for user-specific configuration, which makes it easy to adapt the bot for different users.
- The use of `.env` for secrets is a good security practice.
- The code is procedural, with a clear top-down flow in `main.py`.
- Logging is used to track the bot's activity and the status of each application.
- The project includes a simple dashboard generation script to visualize the results.
