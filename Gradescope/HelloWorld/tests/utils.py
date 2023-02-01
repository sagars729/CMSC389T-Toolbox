import requests
import json
import base64
import os

################ CHANGE BELOW CONSTANTS ###############

# Nothing to Change!

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}

def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def read_submission():
    with open("submission.txt") as submission:
        gh_username = submission.readline().strip()
        gh_repo = submission.readline().strip()
    return gh_username, gh_repo

def response_to_str(response):
    return base64.b64decode(response.json()['content']).decode()
