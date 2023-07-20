import unittest
from unittest.mock import patch, MagicMock
from sonar_downloader import get_orgs, get_projects, download_project_files, download_projects
import requests

class TestSonarDownloader(unittest.TestCase):
    @patch('requests.get')
    def test_get_orgs_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "organizations": [
                {"key": "org1"},
                {"key": "org2"},
            ]
        }
        mock_get.return_value = mock_response

        result = get_orgs()

        self.assertEqual(result, [{"key": "org1"}, {"key": "org2"}])

    @patch('requests.get')
    def test_get_orgs_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "errors": "Not found",
        }
        mock_get.return_value = mock_response

        result = get_orgs()

        self.assertEqual(result, [])

    # Write similar test cases for get_projects, download_project_files, and download_projects functions.

if __name__ == '__main__':
    unittest.main()
