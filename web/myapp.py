# -*- coding: UTF-8 -*-
from couchdb.client import Server
from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)
couch = Server('http://130.220.209.37:5984/')
USER_NAME = 'admin'
USER_PASSWORDS = '940123'
couch.resource.credentials = (USER_NAME, USER_PASSWORDS)
db = couch['tweets_senti_my']   

@app.route('/')
def arch():

    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/driver')
def driver():

    return render_template('driver.html')

@app.route('/malaysia')
def malaysia():

    return render_template('MalaysianGP.html')

@app.route('/singapore')
def singapore():

    return render_template('SingaporeGP.html')

@app.route('/japan')
def japan():

    return render_template('JapanGP.html')


#data API to return the data from couchdb
@app.route('/team_data')
def team_data():
    rows = []
    for row in list(db.view('teamAbout/teamSentiment',group=True)):
            rows.append({'c': [{'v': row.key}, {'v': row.value["Senti"]},{'v': row.value["POS"]},{'v': row.value["NEG"]}]})

    response = {
        'cols': [{'id': 'TeamName', 'label': 'TeamName', 'type': 'string'},
                 {'id': 'sentiment_score', 'label': 'senti_score', 'type': 'number'},
                 {'id': 'tweet_count', 'label': 'tweet_count(POS)', 'type': 'number'},
                 {'id': 'tweet_count', 'label': 'tweet_count(NEG)', 'type': 'number'}
                 ],
        'rows': rows
    }
    return jsonify(response)

@app.route('/driver_data')
def driver_data():
    rows = []
    for row in list(db.view('driverAbout/driverSentiment', group=True)):
        rows.append({'c': [{'v': row.key}, {'v': row.value["Senti"]},{'v': row.value["POS"]},{'v': row.value["NEG"]}]})

    response = {
        'cols': [{'id': 'DriverName', 'label': 'DriverName', 'type': 'string'},
                 {'id': 'sentiment_score', 'label': 'senti_score', 'type': 'number'},
                 {'id': 'tweet_count', 'label': 'tweet_count(POS)', 'type': 'number'},
                 {'id': 'tweet_count', 'label': 'tweet_count(NEG)', 'type': 'number'}
                 ],
        'rows': rows
    }
    return jsonify(response)

@app.route('/Malaysian_data')
def Malaysian_data():
    rows = []
    for row in list(db.view('InterestingEvents/Malaysian', group=True)):
        hour = int(row.key[0])+8
        if(hour > 23):
            hour = hour - 24
        min = row.key[1]
        time = str(hour) + ":" + min
        rows.append({'c': [{'v': time}, {'v': row.value['MP']},{'v': row.value['MN']},{'v': row.value['FP']},{'v': row.value['FN']},{'v': row.value['RP']},{'v': row.value['RN']}]})

    response = {
        'cols': [{'id': 'TimeOfDay', 'label': 'TimeOfDay', 'type': 'string'},
                 {'id': 'MercedesPOS', 'label': 'MercedesPOS', 'type': 'number'},
                 {'id': 'MercedesNEG', 'label': 'MercedesNEG', 'type': 'number'},
                 {'id': 'FerrariPOS', 'label': 'FerrariPOS', 'type': 'number'},
                 {'id': 'FerrariNEG', 'label': 'FerrariNEG', 'type': 'number'},
                 {'id': 'RedBullPOS', 'label': 'RedBullPOS', 'type': 'number'},
                 {'id': 'RedBullNEG', 'label': 'RedBullNEG', 'type': 'number'}
                 ],
        'rows': rows
    }
    return jsonify(response)

@app.route('/Singapore_data')
def Singapore_data():
    rows = []
    for row in list(db.view('InterestingEvents/Singapore',group = True)):
        hour = int(row.key[0])+8
        if(hour > 23):
            hour = hour - 24
        min = row.key[1]
        time = str(hour) + ":" + min
        rows.append({'c': [{'v': time}, {'v': row.value['MP']},{'v': row.value['MN']},{'v': row.value['FP']},{'v': row.value['FN']},{'v': row.value['RP']},{'v': row.value['RN']}]})

    response = {
        'cols': [{'id': 'TimeOfDay', 'label': 'TimeOfDay', 'type': 'string'},
                 {'id': 'MercedesPOS', 'label': 'MercedesPOS', 'type': 'number'},
                 {'id': 'MercedesNEG', 'label': 'MercedesNEG', 'type': 'number'},
                 {'id': 'FerrariPOS', 'label': 'FerrariPOS', 'type': 'number'},
                 {'id': 'FerrariNEG', 'label': 'FerrariNEG', 'type': 'number'},
                 {'id': 'RedBullPOS', 'label': 'RedBullPOS', 'type': 'number'},
                 {'id': 'RedBullNEG', 'label': 'RedBullNEG', 'type': 'number'}
                 ],
        'rows': rows
    }

    return jsonify(response)

@app.route('/Japan_data')
def Japan_data():
    rows = []
    for row in list(db.view('InterestingEvents/Japan',group = True)):
        hour = int(row.key[0])+9
        if(hour > 23):
            hour = hour - 24
        min = row.key[1]
        time = str(hour) + ":" + min
        rows.append({'c': [{'v': time}, {'v': row.value['MP']},{'v': row.value['MN']},{'v': row.value['FP']},{'v': row.value['FN']},{'v': row.value['RP']},{'v': row.value['RN']}]})

    response = {
        'cols': [{'id': 'TimeOfDay', 'label': 'TimeOfDay', 'type': 'string'},
                 {'id': 'MercedesPOS', 'label': 'MercedesPOS', 'type': 'number'},
                 {'id': 'MercedesNEG', 'label': 'MercedesNEG', 'type': 'number'},
                 {'id': 'FerrariPOS', 'label': 'FerrariPOS', 'type': 'number'},
                 {'id': 'FerrariNEG', 'label': 'FerrariNEG', 'type': 'number'},
                 {'id': 'RedBullPOS', 'label': 'RedBullPOS', 'type': 'number'},
                 {'id': 'RedBullNEG', 'label': 'RedBullNEG', 'type': 'number'}
                 ],
        'rows': rows
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True)