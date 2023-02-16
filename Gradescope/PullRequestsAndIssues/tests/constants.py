################ CHANGE BELOW CONSTANTS ###############

ORG = "cmsc389T-spring23" # name of the organization
PR_NUMS = ["1", "2", "3", "4", "5"] # ids of pull requests
PROJECT_NUM = 21 # id of GitHub project board
REPO = "Lecture3" # name of repository

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
