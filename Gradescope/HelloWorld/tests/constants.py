################ CHANGE BELOW CONSTANTS ###############

# Nothing to Change!

###################### END CHANGES ####################

GH_TOKEN = open(".token").readline().strip()
HEADERS = {
  'Authorization': f'Bearer {GH_TOKEN}'
}
