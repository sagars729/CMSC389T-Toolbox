import requests
import json
import base64
import os

################ CHANGE BELOW CONSTANTS ###############

ORG = "cmsc389T-winter23" # name of the organization

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
JUNIT = f"https://github.com/{ORG}/git-java-setup/raw/main/junit-4.10.jar"

def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def request_graphql(data={}):
    return requests.post(f"https://api.github.com/graphql", headers=HEADERS,
                         data=json.dumps(data))

def response_to_str(response):
    return base64.base64.decode(response.json()['content']).decode()

def read_submission():
    with open("submission.txt") as submission:
        gh_username = submission.readline().strip()
        gh_team = submission.readline().strip()
    return gh_username, gh_team

def download_team_repo(team, alias=None):
    if not alias:
      alias = team

    if alias not in os.listdir("."):
      os.system(f"git clone https://{GH_TOKEN}@github.com/{ORG}/{team}.git {alias}")
      os.system(f"cd {alias} && wget {JUNIT}")
