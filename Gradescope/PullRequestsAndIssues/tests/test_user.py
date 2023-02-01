import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility
from utils import request_github, read_submission
import json


class TestUser(unittest.TestCase):
    def setUp(self):
      self.gh_username = read_submission() 
      self.metadata = json.load(open("submission_metadata.json"))
      self.user_email =  self.metadata["users"][0]["email"]
      self.username = self.user_email.split("@")[0]
      self.roster = json.load(open("roster.json"))
 
    @weight(-0.1)
    @number("0.1")
    @visibility('hidden')
    def test_invalid_username(self):
      self.assertIn(self.username, self.roster)
      self.assertNotEqual(self.roster[self.username], self.gh_username)
