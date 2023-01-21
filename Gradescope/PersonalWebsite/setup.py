import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility 

from tests.utils import request_github, post_github, read_submission,\
  read_submission_links, download_repo, push_update
import base64
import json
import time
import requests
import os


def run_workflow(slug, workflow, skip_run=False, max_retries=24):
    if not skip_run:
      resp = post_github(f"repos/{slug}/actions/workflows/{workflow['id']}/dispatches",
                         {'ref': 'main'})
      if resp.status_code//100 != 2:
        print("Workflow was not triggered")
        return {'conclusion': 'failed'}

    time.sleep(5)    

    runs = request_github(f"repos/{slug}/actions/runs",
                          {'actor': 'sagars729', 'branch': 'main'}).json()['workflow_runs']
    runs = [r for r in runs if r['name'] == workflow['name']]

    if len(runs) == 0:
      print("No runs found for workflow")
      return {'conclusion': 'failed'}

    run = runs[0]
    run_id = run['id']

    num_retries = 0
    while run['status'] not in ['completed', 'failed', 'cancelled'] and num_retries < max_retries:
      time.sleep(5)
      run = request_github(f"repos/{slug}/actions/runs/{run_id}").json()
      num_retries += 1

    if num_retries == max_retries:
      print("Maxmimum time limit exceeded")
      return {'conclusion': 'failed'}

    return run

def get_link_status_code(link):
    return requests.get(link).status_code 

def clone_clean_deploy(slug, workflows, terp):
   conclusions = {'clone': False, 'deploy': False, 'clean': False}

   if not terp: return
   page_exists = lambda: get_link_status_code(terp) == 200

   order = ['deploy', 'clean', 'clone'] if page_exists() else ['clone', 'deploy', 'clean']
   print(terp, get_link_status_code(terp))
   print(order, page_exists())
   for w in order:
     if w == "clone":
       if "clone" not in workflows or page_exists():
         continue
       print("cloning")
       run = run_workflow(slug, workflows['clone'])
       conclusions['clone'] = run['conclusion'] == 'success' and page_exists()
     elif w == "clean":
       if "clean" not in workflows or not page_exists():
         continue
       print("cleaning")
       run = run_workflow(slug, workflows['clean'])
       conclusions['clean'] = run['conclusion'] == 'success' and not page_exists()
     else:
       if "deploy" not in workflows or not page_exists():
         continue
       print("deploying")
       download_repo(slug)
       push_update(slug)
       time.sleep(5)
       run = run_workflow(slug, workflows['deploy'], True)
       updated = 'autograder comment' in requests.get(terp).text.lower()
       conclusions['deploy'] = run['conclusion'] == 'success' and updated

   with open("conclusions.json", "w") as outfile:
     json.dump(conclusions, outfile)

if __name__ == "__main__":
    gh_username, gh_repo = read_submission() 
    slug = f"{gh_username}/{gh_repo}"
    workflows = request_github(f"repos/{slug}/actions/workflows").json()['workflows']
    assert len(workflows) >= 4, "Repository has less than 4 workflows"

    pages, terp = read_submission_links(slug)
    print(f"GitHub Pages: {pages}")
    print(f"Terpconnect: {terp}")

    workflow_dict = {}
    for workflow in workflows:
      name = workflow['name'].lower()
      if "docker" in name:
        workflow_dict['docker'] = workflow
      elif "clone" in name:
        workflow_dict['clone'] = workflow
      elif ("deploy" in name and "pages" not in name) or "update" in name:
        workflow_dict['deploy'] = workflow
      elif "clean" in name or "delete" in name:
        workflow_dict['clean'] = workflow
    print(workflow_dict)

    clone_clean_deploy(slug, workflow_dict, terp)
