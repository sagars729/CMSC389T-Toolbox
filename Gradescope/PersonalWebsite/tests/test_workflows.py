import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility 

from utils import request_github, post_github, read_submission,\
  read_submission_links, download_repo, push_update, ORG, TEMPLATE
import base64
import json
import time
import requests
import os


def run_workflow(slug, workflow):
    resp = post_github(f"repos/{slug}/actions/workflows/{workflow['id']}/dispatches",
                       {'ref': 'main'})
    assert resp.status_code//100 == 2, f"Worfklow was not triggered"

    time.sleep(5)    

    runs = request_github(f"repos/{slug}/actions/runs",
                          {'actor': 'sagars729', 'branch': 'main'}).json()['workflow_runs']
    runs = [r for r in runs if r['name'] == workflow['name']]
    assert len(runs) > 0, "No runs found for workflow"

    run = runs[0]
    run_id = run['id']

    while run['status'] not in ['completed', 'failed', 'cancelled']:
      time.sleep(5)
      run = request_github(f"repos/{slug}/actions/runs/{run_id}").json()

    return run


def get_link_status_code(link):
    return requests.get(link).status_code 


class TestWorkflows(unittest.TestCase):

    def clone_clean_deploy(self):
       self.conclusions = {'clone': False, 'deploy': False, 'clean': False}
       with open("conclusions.json", "r") as infile:
          self.conclusions = json.load(infile)
       return

    def setUp(self):
      self.gh_username, self.gh_repo = read_submission() 
      self.slug = f"{self.gh_username}/{self.gh_repo}"
      workflows = request_github(f"repos/{self.slug}/actions/workflows").json()['workflows']
      assert len(workflows) >= 4, "Repository has less than 4 workflows"

      self.pages, self.terp = read_submission_links(self.slug)

      self.workflows = {}
      for workflow in workflows:
        if "docker" in workflow['name'].lower():
          self.workflows['docker'] = workflow
        elif "clone" in workflow['name'].lower():
          self.workflows['clone'] = workflow
        elif "deploy" in workflow['name'].lower():
          self.workflows['deploy'] = workflow
        elif "clean" in workflow['name'].lower():
          self.workflows['clean'] = workflow

      self.clone_clean_deploy()

    @weight(5)
    @number("1.1")
    def test_github_pages_link(self):
      "GitHub Pages Link on README and Live"
      self.assertTrue(self.pages)
      code = get_link_status_code(self.pages)
      self.assertEqual(code, 200, "GitHub Pages is not Live")

    @weight(2)
    @number("1.2")
    def test_terpconnect_link(self):
      "Terpconnect Link on README"
      self.assertTrue(self.terp), "Terpconnect Link Not Found on README"

    @weight(3)
    @number("1.3")
    def test_forked_class_repo(self):
      "Forked Class Repo"
      repo_details = request_github(f"repos/{self.slug}").json()
      self.assertTrue(repo_details['fork'], "Repository was Not Forked")
      self.assertEqual(repo_details['parent']['full_name'].lower(),
                       f"{ORG}/{TEMPLATE}".lower(),
                       "Class Repository was Not Forked")

    @weight(20)
    @number("2.1")
    def test_docker_testing_success(self):
      "Docker Testing Succeeded"
      run = run_workflow(self.slug, self.workflows['docker']) 
      self.assertEqual(run['conclusion'], 'success',
                      "Docker Testing Workflow Failed")

    @weight(10)
    @number("3.1")
    def test_clone_workflow(self):
      "Clone Workflow Succeeded"
      self.assertTrue(self.conclusions['clone'])

    @weight(10)
    @number("3.2")
    def test_deploy_workflow(self):
      "Deploy Workflow Succeeded"
      self.assertTrue(self.conclusions['deploy'])

    @weight(10)
    @number("3.3")
    def test_clean_workflow(self):
      "Clean Workflow Succeeded"
      self.assertTrue(self.conclusions['clean'])
