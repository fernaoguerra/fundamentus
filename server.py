#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from fundamentus import get_data, get_todays_data
from datetime import datetime
import json, csv

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# First update
lista = (get_data())
dia = datetime.strftime(datetime.today(), '%d')

@app.route("/")
@cross_origin()
def json_api():
    global lista, dia    
    # Then only update once a day
    if dia == datetime.strftime(datetime.today(), '%d'):
    	# print('a lista esta ' + lista)
        lista = get_todays_data()
        return (lista)
    else:
        # lista = (get_data())
        lista, dia = (get_data()), datetime.strftime(datetime.today(), '%d')
        #print('a lista esta ' + lista)
        return (lista)

app.run(debug=True, host='0.0.0.0')