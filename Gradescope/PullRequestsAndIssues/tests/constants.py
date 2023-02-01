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
