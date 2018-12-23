from flask import Flask, render_template, url_for
from app import app
from app.graph import *

@app.route('/')
@app.route('/index')
def index():
    graph1_url = allteams
    return render_template('index.html', allteams=graph1_url, teams_dict=teams_dict)

@app.route('/<team>')
def some_place_page(team):
    for k, v in teams_dict.items():
        if v == team:
            global graph1_url
            graph1_url = allteams[k-1]
            break
        else:
            continue
    return render_template('teams.html', allteams=graph1_url, teams_dict=teams_dict)
if __name__ == '__main__':
    app.debug = True
    app.run()
