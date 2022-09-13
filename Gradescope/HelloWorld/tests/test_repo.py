import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

import requests
import base64
import json


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.repo = open("submission.txt").readline().strip()
        self.tokens = self.repo.split("/")
        self.get_slug = lambda : '/'.join(self.tokens[-2:]) 
        self.metadata = json.load(open("/autograder/submission_metadata.json"))

    @weight(0)
    @number("1.1")
    def test_correctly_formatted_repo(self):
        """Check URL Format"""
        self.assertEqual(len(self.tokens), 5, 
                         "URL Format Must Match https://github.com/{owner}/{repo}")

    @weight(0)
    @number("1.2")
    def test_repo_exists(self):
        """Check if Repo Exists"""
        slug = self.get_slug()
        response = requests.get(f"https://api.github.com/repos/{slug}")
        self.assertEqual(response.status_code, 200,
                         "Repository Does Not Exist")
