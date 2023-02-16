################ CHANGE BELOW CONSTANTS ###############

ORG = "cmsc389T-spring23" # name of the organization
PROJECT = "P2" # name of the project folder

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
JUNIT = f"https://github.com/{ORG}/git-java-setup/raw/main/junit-4.10.jar"
