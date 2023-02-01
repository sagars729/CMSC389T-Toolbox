import requests
import json
import base64
import os
import re

from constants import GH_USER, ORG, TEMPLATE, GH_TOKEN, HEADERS


def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def request_graphql(data={}):
    return requests.post(f"https://api.github.com/graphql", headers=HEADERS,
                         data=json.dumps(data))

def post_github(path, data={}):
    return requests.post(f"https://api.github.com/{path}", headers=HEADERS,
                         data=json.dumps(data))

def response_to_str(response):
    return base64.base64.decode(response.json()['content']).decode()

def read_submission():
    with open("submission.txt") as submission:
        gh_username = submission.readline().strip().lower()
        gh_repo = submission.readline().strip()
    return gh_username, gh_repo

def download_readme(slug):
    if "README.md" not in os.listdir("."):
      os.system(f"wget https://raw.githubusercontent.com/{slug}/main/README.md")

def read_submission_links(slug):
    download_readme(slug)

    pages_link, terp_link = None, None
    with open("README.md") as readme:
      lines = [re.sub(r'[\[\]\(\)]', ' ', line) for line in readme]
      lines = [line.split() for line in lines]
      for line in lines:
        for word in line:
          if "github.io" in word: pages_link = word
          if "terpconnect.umd.edu" in word: terp_link = word

    return pages_link, terp_link      

def push_update(slug):
    os.system("cd submission_repo && git config --global user.name cmsc389T-grader-bot")
    os.system("cd submission_repo && git config --global user.email cmsc389T@bot.cmsc389T")
    os.system('cd submission_repo && sed -i".bak" "s/<\/body>/<\!-- Autograder Comment --><\/body>/g" index.html')
    os.system('cd submission_repo && git add index.html')
    os.system('cd submission_repo && git commit -m "autograder commit"')
    os.system(f'cd submission_repo && git push https://{GH_TOKEN}@github.com/{slug}.git')

def download_repo(slug):
    alias = "submission_repo"

    if alias not in os.listdir("."):
      os.system(f"git clone https://{GH_TOKEN}@github.com/{slug}.git {alias}")
