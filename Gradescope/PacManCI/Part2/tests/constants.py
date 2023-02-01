################ CHANGE BELOW CONSTANTS ###############

ORG = "cmsc389T-winter23" # name of the organization

###################### END CHANGES ####################

JUNIT = f"https://github.com/{ORG}/git-java-setup/raw/main/junit-4.10.jar"
GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
