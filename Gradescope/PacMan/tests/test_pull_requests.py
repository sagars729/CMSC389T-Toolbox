import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility 

from utils import request_github, request_graphql, read_submission, ORG
import base64
import json


def load_pull_request_reviews(team, pull_num):
  pull_request_reviews = request_github(
      f"repos/{ORG}/{team}/pulls/{pull_num}/reviews")
  assert pull_request_reviews.status_code == 200, f"No Reviews For PR {pull_num}"

  pull_request_reviews = pull_request_reviews.json()
  pull_request_reviews = {
    review["user"]["login"]: {
      "body": review["body"],
      "state": review["state"]
    } 
  for review in pull_request_reviews}

  return pull_request_reviews

def load_pull_requests(user, team):
  # load team pull requests
  pull_requests = request_github(
      f"repos/{ORG}/{team}/pulls", {"state": "all", "per_page": 100})
  assert pull_requests.status_code == 200, f"No Pull Requests for Team {team}"
  pull_requests = pull_requests.json()
  assert len(pull_requests) > 0, f"No Pull Requests for Team {team}"

  # filter fields
  pull_requests = [{
    "id": pr["html_url"].split("/")[-1],
    "url": pr["html_url"],
    "assignee": pr["assignees"][0]["login"] if len(pr["assignees"]) > 0 else None,
    "title": pr["title"],
    "state": pr["state"],
    "body": pr["body"],
    "merge_commit": pr["merge_commit_sha"],
    "head": pr["head"]["ref"].lower(),
    "base": pr["base"]["ref"].lower(),
    "reviewers": [r["login"] for r in pr["requested_reviewers"]]
  } for pr in pull_requests]

  # load reviewers that have reviewed
  for pr in pull_requests:
    pull_request_reviews = load_pull_request_reviews(team, pr["id"])
    pr["reviewers"] += [login for login in pull_request_reviews]
    pr["approved"] = max([pull_request_reviews[login]["state"] == "APPROVED"
                          for login in pull_request_reviews] + [False])
    pr["reviewer_states"] = pull_request_reviews

  return pull_requests

class TestPullRequests(unittest.TestCase):

    def setUp(self):
      self.gh_username, self.gh_team = read_submission() 
      self.pull_requests = load_pull_requests(self.gh_username, self.gh_team)
      self.bases = set([pr["base"] for pr in self.pull_requests])

      self.assigned = {base:False for base in self.bases}
      self.reviewers = {base:[] for base in self.bases}
      self.approved = {base:False for base in self.bases}
      self.merged = {base:False for base in self.bases}
      self.reviewed = {base:False for base in self.bases}

      # manual grading help string
      self.help_str = "******* MANUAL GRADING LINKS *******\n"

      # populate reviewers
      for pr in self.pull_requests:
        if not pr["merge_commit"]: continue
        if pr["assignee"] == self.gh_username:
          self.reviewers[pr["base"]] += pr["reviewers"]
          self.approved[pr["base"]] = self.approved[pr["base"]] or pr["approved"]
          self.merged[pr["base"]] = True
          self.assigned[pr["base"]] = True
          self.help_str += f'{pr["title"]} - {pr["url"]}\n'
        elif (self.gh_username in pr["reviewer_states"] and
              pr["reviewer_states"][self.gh_username]["state"] == "APPROVED"):
          self.reviewed[pr["base"]] = True

      self.help_str += "******* END MANUAL GRADING LINKS *******"

    @weight(0)
    @number("0.1")
    @visibility("hidden")
    def test_log_manual_grading_links(self):
      print(self.help_str)    
 
    @weight(3)
    @number("1.1")
    def test_assigned_pacman_pull_request(self):
      "Assigned to PacMan FTR-item -> FTR Pull Request"
      self.assertTrue(self.assigned["ftr-pacman"],
                      "Not assigned to a PacMan FTR item Request")
        
    @weight(3)
    @number("1.2")
    def test_assigned_ghost_pull_request(self):
      "Assigned to Ghost FTR-item -> FTR Pull Request"
      self.assertTrue(self.assigned["ftr-ghost"],
                     "Not assigned to a Ghost FTR item Request")
        
    @weight(3)
    @number("1.3")
    def test_assigned_map_pull_request(self):
      "Assigned to Map FTR-item -> FTR Pull Request"
      self.assertTrue(self.assigned["ftr-map"],
                      "Not assigned to a Map FTR item Pull Request")
     
    @weight(2)
    @number("1.4")
    def test_requested_reviewers_pacman_pull_request(self):
      "Requested Reviewers to PacMan FTR-item -> FTR Pull Request"
      self.assertTrue(self.reviewers["ftr-pacman"],
                      "No reviewers on PacMan FTR-item Pull Requests")

    @weight(2)
    @number("1.5")
    def test_requested_reviewers_ghost_pull_request(self):
      "Requested Reviewers to Ghost FTR-item -> FTR Pull Request"
      self.assertTrue(self.reviewers["ftr-ghost"],
                      "No reviewers on Ghost FTR-item Pull Requests")
     
    @weight(2)
    @number("1.6")
    def test_requested_reviewers_map_pull_request(self):
      "Requested Reviewers to Map FTR-item -> FTR Pull Request"
      self.assertTrue(self.reviewers["ftr-map"],
                      "No reviewers on Map FTR-item Pull Requests")

    @weight(2)
    @number("2.1")
    def test_approved_before_merge_pacman_pull_request(self):
      "Approval Before Merge for PacMan FTR-item -> FTR Pull Request"
      self.assertTrue(self.approved["ftr-pacman"])

    @weight(2)
    @number("2.2")
    def test_approved_before_merge_ghost_pull_request(self):
      "Approval Before Merge for Ghost FTR-item -> FTR Pull Request"
      self.assertTrue(self.approved["ftr-ghost"])

    @weight(2)
    @number("2.3")
    def test_approved_before_merge_map_pull_request(self):
      "Approval Before Merge for Map FTR-item -> FTR Pull Request"
      self.assertTrue(self.approved["ftr-map"])

    @weight(3)
    @number("2.4")
    def test_merged_pacman_pull_request(self):
      "Merged PacMan FTR-item -> FTR Pull Request"
      self.assertTrue(self.merged["ftr-pacman"])

    @weight(3)
    @number("2.5")
    def test_merged_ghost_pull_request(self):
      "Merged for Ghost FTR-item -> FTR Pull Request"
      self.assertTrue(self.approved["ftr-ghost"])

    @weight(3)
    @number("2.6")
    def test_merged_map_pull_request(self):
      "Merged for Map FTR-item -> FTR Pull Request"
      self.assertTrue(self.approved["ftr-map"])

    @weight(5)
    @number("3.1")
    def test_approved_pacman_pull_request(self):
      "Approved PacMan FTR-item -> FTR Pull Request"
      self.assertTrue(self.reviewed["ftr-pacman"])

    @weight(5)
    @number("3.2")
    def test_approved_ghost_pull_request(self):
      "Approved Ghost FTR-item -> FTR Pull Request"
      self.assertTrue(self.reviewed["ftr-ghost"])

    @weight(5)
    @number("3.3")
    def test_approved_map_pull_request(self):
      "Approved Map FTR-item -> FTR Pull Request"
      self.assertTrue(self.reviewed["ftr-map"])
