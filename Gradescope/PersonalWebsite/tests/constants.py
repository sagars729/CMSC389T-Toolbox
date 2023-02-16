################ CHANGE BELOW CONSTANTS ###############

GH_USER = "sagars729" # user the gh token belongs to
ORG = "cmsc389T-winter23" # name of the organization
TEMPLATE = "cmsc389T-web-template" # name of the template repo

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
