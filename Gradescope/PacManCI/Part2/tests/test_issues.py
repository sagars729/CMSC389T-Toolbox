import unittest
from gradescope_utils.autograder_utils.decorators import weight, number

from utils import request_github, request_graphql, read_submission, ORG
import base64
import json


def get_project_id(team):
  projects = request_graphql({'query':
      """
      query {
        organization(login: \"%s\") {
          projectsV2(first: 50) {
            nodes {
              id
              title
            }
          }
        }
      }
      """ % (ORG)
  }).json()['data']['organization']['projectsV2']['nodes']

  projects = [project for project in projects
              if project['title'].lower() == f'{team} PacMan CI Backlog'.lower()]

  assert len(projects) > 0, f'Project "{team} PacMan CI Backlog" Not Found'
  return projects[0]['id']


def load_project_cards(project_id):
  project_cards = request_graphql({'query':
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
      """ % (project_id)
  }).json()['data']['node']['items']['nodes']

  # restructure cards
  project_cards = [{
    "assignee": card['content']['assignees']['nodes'][0]['login'],
    "title": card['content']['title'],
    "body": card['content']['body']
  } for card in project_cards
    if 'assignees' in card['content'] and
    len(card['content']['assignees']['nodes']) > 0]

  assert len(project_cards) > 0, f'No cards found for project "{project_id}"'

  return project_cards

class TestIssues(unittest.TestCase):

    def setUp(self):
      self.gh_username, self.gh_team = read_submission()
      self.project_id = get_project_id(self.gh_team)
      self.cards = load_project_cards(self.project_id)

      self.cards = [card for card in self.cards
                    if card['assignee'] == self.gh_username]
      self.card_titles = [card['title'].lower() for card in self.cards]

    @weight(5)
    @number("4.1")
    def test_assigned_to_fix_issue_card(self):
      "Created a Fix Issue Card and Assigned Themselves"
      self.assertIn("fix", ' '.join(self.card_titles))
