import requests
import json
import base64

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
ORG = "cmsc389T-winter23"
PR_NUMS = ["4", "5", "6", "7"]
PROJECT_NUM = 13

def request_github(path, params={}):
    return requests.get(f"https://api.github.com/{path}", headers=HEADERS, params=params)

def request_graphql(data={}):
    return requests.post(f"https://api.github.com/graphql", headers=HEADERS,
                         data=json.dumps(data))

def response_to_str(response):
    return base64.base64.decode(response.json()['content']).decode()

