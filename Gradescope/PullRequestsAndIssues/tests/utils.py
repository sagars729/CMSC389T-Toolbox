import requests
import json
import base64

################ CHANGE BELOW CONSTANTS ###############

ORG = "cmsc389T-winter23" # name of the organization
PR_NUMS = ["4", "5", "6", "7"] # ids of pull requests
PROJECT_NUM = 13 # id of GitHub project board
REPO = "Lecture2" # name of repository

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}

def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def request_graphql(data={}):
    return requests.post(f"https://api.github.com/graphql", headers=HEADERS,
                         data=json.dumps(data))

def response_to_str(response):
    return base64.base64.decode(response.json()['content']).decode()

