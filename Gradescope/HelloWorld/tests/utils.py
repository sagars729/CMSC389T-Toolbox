import requests
import json
import base64
import os

from constants import HEADERS


def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def read_submission():
    with open("submission.txt") as submission:
        gh_username = submission.readline().strip()
        gh_repo = submission.readline().strip()
    return gh_username, gh_repo

def response_to_str(response):
    return base64.b64decode(response.json()['content']).decode()
