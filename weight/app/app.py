"""
Weight Application
------------------
  The industrial weight is in charge of weighing trucks, allowing payment to providers.
  The WeightApp tracks all weights and allows payment to be for net weight.
  Reminder: Bruto = Neto (fruit) + Tara (truck) + sum(Tara(Containers))
"""

# -*-coding:utf-8 -*
#from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mySQL_DAL
from pathlib import Path
from typing import List, Dict
import csv
import datetime
import logging
import mysql.connector
import os
import uuid


# Setting .env path and loading its values
#env_path = Path('.') / '.env'
#load_dotenv(dotenv_path=env_path, verbose=True, override=True)

# Logging default level is WARNING (30), So switch to level DEBUG (10)
logging.basicConfig(filename = 'test.log', level = logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

app = Flask(__name__)

def init_config() -> List[Dict]:
    # configures and initializes MySQL database.
    config = {
    'user' : os.getenv('USER'),
    'password' : os.getenv('PASSWORD'),
    'host' : os.getenv('HOST'),
    'port' : os.getenv('PORT'),
    'database' : os.getenv('DATABASE')
    }
    conn = mysql.connector.connect(**config)
    cur = conn.cur()
    cur.execute('SELECT * From weighings')
    logging.debug(cur)
    cur.close()
    conn.close()
    return res

def csv_to_json(csvFile):
    """
    takes an input CSV file and returns its JSON representation.
    """
    data = []
    with open(csvFile) as f:
        for row in csv.DictReader(f):
            data.append(row)
    json_data = json.dumps(data)
    return json_data

@app.route('/')
def index() -> str:
    """
    for debugging purposes: dumps all database.
    """
    return json.dumps({'weight_system': init_config()})

@app.route('/weight', methods = ['POST'])
def post_weight():
    """
    Note that "in" & "none" will generate a new session id, and "out" will return session id of previous "in" for the truck.
    Return json on success:
    {
      "id": <str>,
      "truck": <license> or "na",
      "bruto": <int>,
      //ONLY for OUT:
      "truckTara": <int>,
      "neto": <int> or "na" // na if some of containers have unknown tara
    }
    """
    direction = request.args.get('direction')
    truck_id = request.args.get('truck')
    container_ids = request.args.get('containers')
    weight = request.args.get('weight')
    unit = request.args.get('unit')
    force = request.args.get('force')
    produce = request.args.get('produce')
    # post values to db
    
    # return json on success
    pass  # temporary line, until function and return implemented

@app.route('/batch-weight?file=<string:filename>', methods = ['POST'])
def post_batch_weight(filename):
    """
    Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers.
    File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    """
    # do something with parameter `filename`
    if filename.endswith('.csv'):
        jsonData = csv_to_json(filename)
    elif filename.endswith('.json'):
        with open(filename, 'r') as f:
            jsonData = f.readlines()
    else:
        return 'Error: illegal filetype.'

    print(jsonData)

    return 'ok'

@app.route('/unknown', methods = ['GET'])
def get_unknown_containers():
    """
    Returns a list of all recorded containers that have unknown weight:
    ["id1","id2",...]
    """
    unknown_container_arr = mySQL_DAL.get_unknown_weight_containers()
    return unknown_container_arr

@app.route('/weight?from=<string:t1>&to=<string:t2>&filter=<string:filter>', methods = ['GET'])  # /weight?from=t1&to=t2&filter=f
def get_weighings_from_dt(t1, t2, directions = ['in', 'out', 'none']):
    """
    - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
    - directions - comma delimited list of directions. default is "in,out,none"
    default t1 is "today at 000000". default t2 is "now".
    returns an array of json objects, one per weighing (batch NOT included)
    """
    
    # return array of json objects
    pass  # temporary line, until function and return implemented

@app.route('/item/<string:id>?from=<string:t1>&to=<string:t2>', methods = ['GET'])  # /item/<id>?from=t1&to=t2
def get_item(item_id, t1, t2):
    """
    - id is for an item (truck or container). 404 will be returned if non-existent
    - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
    default t1 is "1st of month at 000000". default t2 is "now".
    Returns a json:
    {
      "id": <str>,
      "tara": <int> OR "na", // for a truck this is the "last known tara"
      "sessions": [ <id1>,...]
    }
    """
    
    # return json
    pass  # temporary line, until function and return implemented

@app.route('/session/<string:id>', methods = ['GET'])  # /session/<id>
def get_session(session_id):
    """
    session_id is for a weighing session. 404 will be returned if non-existent.
    Returns a json:
    {
      "id": <str>,
      "truck": <truck-id> or "na",
      "bruto": <int>,
      //ONLY for OUT:
      "truckTara": <int>,
      "neto": <int> or "na" // na if some of containers unknown
    }
    """
    
    # return json
    pass  # temporary line, until function and return implemented

@app.route('/health', methods = ['GET'])
def health():
    """
    health function...
    """
    # test read from /in directory
    # test acess to database
    # other tests...
    return "ok"
    pass  # temporary line, until function and return implemented


if __name__ == '__main__':
    logging.info('Starting Flask server...')
    app.run(host='0.0.0.0', debug=True, port=5000)
