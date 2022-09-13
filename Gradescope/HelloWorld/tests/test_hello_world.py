import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

import requests
import base64
import json


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.repo = open("submission.txt").readline().strip()
        self.tokens = self.repo.split("/")
        self.get_slug = lambda : '/'.join(self.tokens[-2:]) 

    @weight(5)
    @number("2.1")
    def test_file_contains_hello_world(self):
        """Check if test.txt is correct"""
        slug = self.get_slug()
        response = requests.get(f"https://api.github.com/repos/{slug}/contents/test.txt")
        self.assertEqual(response.status_code, 200,
                         "README Does Not Exist")
        text = base64.b64decode(response.json()['content']).decode()
        self.assertIn("Hello World", text, "test.txt does not contain Hello World")
