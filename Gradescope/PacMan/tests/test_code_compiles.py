import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

from utils import download_team_repo, read_submission
from constants import PROJECT

import base64
import json
import os


class TestCodeCompiles(unittest.TestCase):

    def setUp(self):
      self.gh_username, self.gh_team = read_submission()

    @weight(5)
    @number("5.1")
    def test_source_code_compiles(self):
      "Team Source Code Compiles"
      download_team_repo(self.gh_team, f"{self.gh_team}-src")
      status = os.system(f'cd {self.gh_team}-src/Projects/{PROJECT} && javac -cp "src/" src/*.java')
      self.assertEqual(status, 0, "Team source code did not compile")
     

    @weight(5)
    @number("5.2")
    def test_test_code_compiles(self):
      "Team Test Code Compiles"
      download_team_repo(self.gh_team, f"{self.gh_team}-test")
      status = os.system(f'cd {self.gh_team}-src/Projects/{PROJECT} && javac -cp "src/:tests/:../../junit-4.10.jar" src/*.java tests/*.java')
      self.assertEqual(status, 0, "Team source and test code did not compile")
