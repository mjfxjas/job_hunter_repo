# Job Hunter

Python scripts for finding LinkedIn jobs, generating cover letters with Claude,
and attempting Easy Apply submissions. Application status is stored in
`applications.csv`; cover letters are saved in `cover_letters/`.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file containing `ANTHROPIC_API_KEY`, `LINKEDIN_EMAIL`, and
`LINKEDIN_PASSWORD`. Update `profile.py` with your experience and target roles.

## Run

```bash
python main.py
```

The current entry point searches for up to 10 jobs per run. It skips jobs already
recorded as submitted or applied, generates cover letters, and attempts to fill
and submit applications. Applications marked `partial` need manual completion.

## Tests

```bash
python -m unittest discover -s tests -v
```

The logger tests use temporary CSV files. The other integration scripts can
access LinkedIn, call Claude, or submit applications.
