import requests
import json
import base64

from constants import HEADERS

def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def request_graphql(data={}):
    return requests.post(f"https://api.github.com/graphql", headers=HEADERS,
                         data=json.dumps(data))

def read_submission():
    with open("submission.txt") as submission:
        gh_username = submission.readline().strip().lower()
    return gh_username

def response_to_str(response):
    return base64.base64.decode(response.json()['content']).decode()

