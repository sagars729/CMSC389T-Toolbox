import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

from utils import request_github, request_graphql, read_submission
from constants import ORG, PR_NUMS, PROJECT_NUM, REPO


class TestPullRequestsAndIssues(unittest.TestCase):
    def load_pull_request_reviews(self, pull_num):
      # load reviewers
      pull_request = request_github(
          f"repos/{ORG}/{REPO}/pulls/{pull_num}")
      self.assertEqual(pull_request.status_code, 200,
                       f"Unable To Find Pull Request {pull_num}")
      self.requested_reviewers += [r.lower() for r in 
        pull_request.json()["requested_reviewers"]]

      # load reviewer comments and status
      pull_request_reviews = request_github(
          f"repos/{ORG}/{REPO}/pulls/{pull_num}/reviews", {'per_page': 80})
      self.assertEqual(pull_request_reviews.status_code, 200,
                  "Unable To Find Pull Request Reviews")
      pull_request_reviews = pull_request_reviews.json()
      pull_request_reviews = {review["user"]["login"].lower(): {
          "body": review["body"], "state": review["state"]}
          for review in pull_request_reviews}
      self.pull_request_reviews.update(pull_request_reviews)

    def setUp(self):
      self.gh_username = read_submission()

      # load pull request reviews
      self.requested_reviewers = []
      self.pull_request_reviews = {}
      for pull_num in PR_NUMS:
        self.load_pull_request_reviews(pull_num)

      # load project cards
      self.project_id = request_graphql({'query':
          """
          query {
            organization(login: \"%s\") {
              projectV2(number: %d) {
                id
              }
            }
          }
          """ % (ORG, PROJECT_NUM)
      }).json()['data']['organization']['projectV2']['id']
      self.project_cards = request_graphql({'query':
          """
          query {
            node(id: \"%s\") {
              ... on ProjectV2 {
                items (first: 100) {
                  nodes {
                    content {
                      ... on Issue {
                        title
                        body
                        assignees(first: 1) {
                          nodes {
                            login
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
          """ % (self.project_id)
      }).json()['data']['node']['items']['nodes']
      self.project_cards = {card['content']['assignees']['nodes'][0]['login']:
        {'title': card['content']['title'], 'body': card['content']['body']}
        for card in self.project_cards
        if 'assignees' in card['content'] and 
        len(card['content']['assignees']['nodes']) > 0}
      
    @weight(1)
    @number("1.1")
    def test_added_as_reviewer(self):
      "Added as a Reviewer"
      reviewers = [r["login"] for r in self.requested_reviewers
                  ] + [login for login in self.pull_request_reviews]
      self.assertIn(self.gh_username, reviewers,
                    f"{self.gh_username} is not a reviewer")

    @weight(2)
    @number("1.2")
    def test_left_a_comment(self):
      "Left a Comment"
      self.assertIn(self.gh_username, self.pull_request_reviews,
                    f"{self.gh_username} has not left a review")
      self.assertNotEqual(self.pull_request_reviews[self.gh_username]["body"],
                          "", f"{self.gh_username} has not left a comment")
                          
    @weight(2)
    @number("1.3")
    def test_approved_pull_request(self):
      "approved the pull request"
      self.assertIn(self.gh_username, self.pull_request_reviews,
                    f"{self.gh_username} has not left a review")
      self.assertEqual(self.pull_request_reviews[self.gh_username]["state"], "APPROVED",
                       f"{self.gh_username} has not approved")
                          
    @weight(2)
    @number("2.1")
    def test_created_and_assigned_card(self):
      "created a card"
      self.assertIn(self.gh_username, self.project_cards,
                    f"{self.gh_username} has not been assigned to a card")
                          
    @weight(2)
    @number("2.2")
    def test_descriptive_card_title(self):
      "created a descriptive card title"
      self.assertIn(self.gh_username, self.project_cards,
                    f"{self.gh_username} has not been assigned to a card")
      self.assertIn("First Card", self.project_cards[self.gh_username]['title'],
                    "Missing title in format: {your name} - First Card")

    @weight(1)
    @number("2.3")
    def test_pull_request_linked(self):
      "pull request is linked to issue"
      pass
      
