#import matplotlib.pyplot as plt
import requests
import json

# Incomplete URLS
FPL_URL = "https://fantasy.premierleague.com/drf/"
ALL_DATA_SUBURL = "bootstrap-static"
ALL_DATA_SUBURL_D = "bootstrap-dynamic"
SPECIFIC_PLAYER_SUBURL = "element-summary/1"

# Complete URLS
ALL_DATA_URL = FPL_URL + ALL_DATA_SUBURL
ALL_DATA_URL_D = FPL_URL + ALL_DATA_SUBURL_D
SPECIFIC_PLAYER_URL = FPL_URL + SPECIFIC_PLAYER_SUBURL

# Retrieve data about all teams/players 
r = requests.get(ALL_DATA_URL)
#r.content.decode("utf-8")
return_code = r.status_code
data = r.json()

# Checks return code and prints message for it
if return_code == 200:
    print('Connected successfully')
elif return_code == 301:
    print('Redirecting...')
elif return_code == 404:
    print('Resource not found')
else:
    print('Other issues')

# Create dict with all PL teams and assign their ID
def getAllTeams():
    teams_dict = {} 
    for key in data['teams']:
        teams_dict[key['name']] = key['id']
    return teams_dict
