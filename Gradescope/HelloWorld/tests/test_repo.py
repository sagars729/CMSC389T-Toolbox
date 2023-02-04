import unittest
from gradescope_utils.autograder_utils.decorators import weight, number
from utils import read_submission, request_github


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.username, self.repo = read_submission()

    @weight(0)
    @number("1.1")
    def test_repo_exists(self):
        """Check if Repo Exists"""
        response = request_github(f"repos/{self.username}/{self.repo}")
        self.assertEqual(response.status_code, 200,
                         "Repository Does Not Exist")
