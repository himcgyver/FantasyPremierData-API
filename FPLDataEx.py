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
        
# Retrieve data about all teams/players
def extract_all_data():
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
    return(data)

#####################################################
# Create dict with all PL teams and assign their ID #
#####################################################
data = extract_all_data()
teams_dict = {} 
for key in data['teams']:
    teams_dict[key['id']] = key['name']

# Create dict with player info and it's stats, write graph img to allteams[]
types = []
x_axis = []
y_axis = []
allteams = []
for tkey, tvalue in teams_dict.items():
    for ekey in data['elements']:
        if ekey['team'] == tkey:
            if ekey['minutes'] < 1000:
                continue
            else:
                types.extend([ekey['web_name']])
                x_axis.extend([ekey['minutes']])
                y_axis.extend([ekey['goals_conceded']])
    for i, name in enumerate(types):
        x = x_axis[i]
        y = y_axis[i]
        #Ideti f-cija kad nesioverlappintu vardai

        plt.text(x, y, name, fontsize=7)
        
    plt.scatter(x_axis, y_axis, marker='x', color='red')
    plt.title(tvalue)
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
