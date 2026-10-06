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

    def test_tracking_and_search_urls_share_linkedin_job_identity(self):
        job = {'title': 'Test role', 'company': 'Example',
               'url': 'https://www.linkedin.com/jobs/search/?keywords=Python&currentJobId=123456',
               'source': 'LinkedIn'}
        with tempfile.TemporaryDirectory() as directory:
            logger = ApplicationLogger(Path(directory) / 'applications.csv')
            logger.log(job, 'submitted')
            for url in (
                'https://www.linkedin.com/jobs/view/123456/?trackingId=abc',
                'https://linkedin.com/jobs/view/developer-at-example-123456',
                'https://www.linkedin.com/jobs/search/?currentJobId=123456&keywords=Cloud',
            ):
                with self.subTest(url=url):
                    self.assertTrue(logger.already_applied(url))
            self.assertFalse(logger.already_applied('https://www.linkedin.com/jobs/view/654321'))
            self.assertFalse(logger.already_applied('https://linkedin.com.example.test/jobs/view/123456'))

    def test_other_providers_keep_meaningful_query_parameters(self):
        job = {'title': 'Test role', 'company': 'Example',
               'url': 'https://example.test/careers?job=1', 'source': 'test'}
        with tempfile.TemporaryDirectory() as directory:
            logger = ApplicationLogger(Path(directory) / 'applications.csv')
            logger.log(job, 'submitted')
            self.assertTrue(logger.already_applied(job['url']))
            self.assertFalse(logger.already_applied('https://example.test/careers?job=2'))

    def test_failed_application_can_be_retried(self):
        job = {'title': 'Test role', 'company': 'Example',
               'url': 'https://example.test/jobs/1', 'source': 'test'}
        with tempfile.TemporaryDirectory() as directory:
            logger = ApplicationLogger(Path(directory) / 'applications.csv')
            logger.log(job, 'failed')
            self.assertFalse(logger.already_applied(job['url']))


if __name__ == '__main__':
    unittest.main()
