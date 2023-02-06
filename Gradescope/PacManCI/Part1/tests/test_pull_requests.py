import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility 

from utils import request_github, request_graphql, read_submission
from constants import ORG


def load_pull_request_reviews(slug, pull_num):
  pull_request_reviews = request_github(
      f"repos/{slug}/pulls/{pull_num}/reviews")
  assert pull_request_reviews.status_code == 200, f"No Reviews For PR {pull_num}"

  pull_request_reviews = pull_request_reviews.json()
  pull_request_reviews = {
    review["user"]["login"]: {
      "body": review["body"],
      "state": review["state"]
    } 
  for review in pull_request_reviews}

  return pull_request_reviews

def load_pull_requests(user, slug):
  # load team pull requests
  pull_requests = request_github(
      f"repos/{slug}/pulls", {"state": "all", "per_page": 100})
  assert pull_requests.status_code == 200, f"No Pull Requests for Team {slug}"
  pull_requests = pull_requests.json()
  assert len(pull_requests) > 0, f"No Pull Requests for Team {slug}"

  # filter fields
  pull_requests = [{
    "id": pr["html_url"].split("/")[-1],
    "url": pr["html_url"],
    "assignee": pr["assignees"][0]["login"].lower() if len(pr["assignees"]) > 0 else None,
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
    pull_request_reviews = load_pull_request_reviews(slug, pr["id"])
    pr["reviewers"] += [login for login in pull_request_reviews]
    pr["approved"] = max([pull_request_reviews[login]["state"] == "APPROVED"
                          for login in pull_request_reviews] + [False])
    pr["reviewer_states"] = pull_request_reviews

  return pull_requests

class TestPullRequests(unittest.TestCase):

    def setUp(self):
      self.gh_username, self.gh_team = read_submission() 
      self.pull_requests = load_pull_requests(self.gh_username, f'{ORG}/{self.gh_team}')
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
    def test_assigned_actions_pull_request(self):
      "Created a Pull-Request for your Action FTR-item branch to -> FTR-Action and assigned yourself to the PR"
      self.assertTrue(self.assigned["ftr-actions"],
                      "Not assigned to a Action FTR item Pull Request OR Pull Request made to merge to the Wrong Branch (Must be to FTR-Action)")
        
    @weight(3)
    @number("1.2")
    def test_assigned_sabotage_pull_request(self):
      "Created a Pull-Request for your Sabotage FTR-item branch to -> FTR-Sabotage and assigned yourself to the PR"
      self.assertTrue(self.assigned["ftr-sabotage"],
                     "Not assigned to a Sabotage FTR item Pull Request OR Pull Request made to merge to the Wrong Branch (Must be to FTR-Sabotage)")
        
    @weight(2)
    @number("1.4")
    def test_requested_reviewers_actions_pull_request(self):
      "Requested Reviewers to review your Actions FTR-item -> FTR-Action Pull Request"
      self.assertTrue(self.reviewers["ftr-actions"],
                      "No reviewers assigned on Actions FTR-item Pull Requests (right column Reviewers missing reviewer)")

    @weight(2)
    @number("1.5")
    def test_requested_reviewers_sabotage_pull_request(self):
      "Requested Reviewers to review your Sabotage FTR-item -> FTR-Sabotage Pull Request"
      self.assertTrue(self.reviewers["ftr-sabotage"],
                      "No reviewers assigned on Sabotage FTR-item Pull Requests (right column Reviewers missing reviewer)")
     
    @weight(2)
    @number("2.1")
    def test_approved_before_merge_actions_pull_request(self):
      "Pull Request for your Actions FTR-item -> FTR-Action was approved by assigned reviewer before merging"
      self.assertTrue(self.approved["ftr-actions"],
                      "Pull Request was NOT approved before being merged")

    @weight(2)
    @number("2.2")
    def test_approved_before_merge_sabotage_pull_request(self):
      "Pull Request for your Sabotage FTR-item -> FTR-Sabotage was approved by assigned reviewer before merging"
      self.assertTrue(self.approved["ftr-sabotage"],
                      "Pull Request was NOT approved before being merged")

    @weight(3)
    @number("2.4")
    def test_merged_pacman_pull_request(self):
      "Merged Actions FTR-item -> FTR Pull Request"
      self.assertTrue(self.merged["ftr-actions"],
                      "Actions FTR-item was not merged to FTR-Actions (must be merged to FTR-Pacman)")


    @weight(3)
    @number("2.5")
    def test_merged_sabotage_pull_request(self):
      "Merged Sabotage FTR-item -> FTR Pull Request"
      self.assertTrue(self.approved["ftr-sabotage"],
                      "Sabotage FTR-item was not merged to FTR-Sabotage (must be merged to FTR-Pacman)")


    @weight(5)
    @number("3.1")
    def test_approved_actions_pull_request(self):
      "Approved Actions FTR-item -> FTR Pull Request of another team member "
      self.assertTrue(self.reviewed["ftr-actions"],
                      "Was not assigned as reviewer OR did not approve a Actions FTR-item -> FTR-Action pull request")

    @weight(5)
    @number("3.2")
    def test_approved_sabotage_pull_request(self):
      "Approved Sabotage FTR-item -> FTR Pull Request of another team member"
      self.assertTrue(self.reviewed["ftr-sabotage"],
                      "Was not assigned as reviewer OR did not approve a Sabotage FTR-item -> FTR-Sabotage pull request")
