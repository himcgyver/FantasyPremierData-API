import matplotlib       #sprendimas del error:
matplotlib.use('Agg')   #RuntimeError: main thread is not in main loop
import matplotlib.pyplot as plt
import io
import base64
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

def clearList(names):
    for item in names:
        item.clear()

def extract_all_data():
    # Retrieve data about all teams/players #
    r = requests.get(ALL_DATA_URL)
    return_code = r.status_code
    data = r.json()

    # Checks return code and prints message for it #
    if return_code == 200:
        print('Connected successfully')
    elif return_code == 301:
        print('Redirecting...')
    elif return_code == 404:
        print('Resource not found')
    else:
        print('Other issues')

    return(data)

#####################################################
# Create dict with all PL teams and assign their ID #
#####################################################
data = extract_all_data()

# Create dict with player info and it's stats
allteams = []
info = {}
for teams in data['teams']: #20 teams
    for player_list in data['elements']: #567 players
        if player_list['team'] == teams['id']:
            if player_list['minutes'] < 1000:
                continue
            else:
                info[player_list['web_name']] = [player_list['minutes'], player_list['goals_conceded']]
    x_axis = [v[0] for (k,v) in info.items()]
    y_axis = [v[1] for (k,v) in info.items()]            
    for i, name in enumerate(types):
        x = values[0]   #min played
        y = values[1]   #goals conc.
        plt.text(x, y, name, fontsize=7)
    plt.grid(True)
    plt.scatter(x_axis, y_axis, marker='x', color='red')
    plt.title(teams['name'])
    plt.xlabel("Minutes Played")
    plt.ylabel("Goals Conceded")
    #Convert to image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    clearList([types, x_axis, y_axis])
    allteams.append('data:image/png;base64,{}'.format(graph_url))
