import tempfile
import unittest
from pathlib import Path

from logger import ApplicationLogger


class ApplicationLoggerTests(unittest.TestCase):
    def test_previously_applied_job_is_not_revisited(self):
        job = {'title': 'Test role', 'company': 'Example',
               'url': 'https://example.test/jobs/1', 'source': 'test'}
        with tempfile.TemporaryDirectory() as directory:
            log_path = Path(directory) / 'applications.csv'
            logger = ApplicationLogger(log_path)
            logger.log(job, 'already_applied')

            # Reopening the persisted log matches the next invocation of main.
            next_run = ApplicationLogger(log_path)
            self.assertTrue(next_run.already_applied(job['url']))
            self.assertFalse(next_run.already_applied('https://example.test/jobs/2'))

    def test_failed_application_can_be_retried(self):
        job = {'title': 'Test role', 'company': 'Example',
               'url': 'https://example.test/jobs/1', 'source': 'test'}
        with tempfile.TemporaryDirectory() as directory:
            logger = ApplicationLogger(Path(directory) / 'applications.csv')
            logger.log(job, 'failed')
            self.assertFalse(logger.already_applied(job['url']))


if __name__ == '__main__':
    unittest.main()
