# -*-coding:utf-8 -*
from typing import List, Dict
from pathlib import Path  # python3 only
from flask import Flask, request, json, jsonify
import os
import logging
import mysql.connector
import uuid
import csv
import code
import pdb

# Setting .env path and loading its values
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True, override=True)

# Logging default level is WARNING (30), So switch to level DEBUG (10)
logging.basicConfig(filename="test.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s")


app = Flask(__name__)


# Team: Michael, Raphael, Moria

"""
Weight Application
------------------
  The industrial weight is in charge of weighing trucks, allowing payment to providers.
  The WeightApp tracks all weights and allows payment to be for net weight.
  Reminder: Bruto = Neto (fruit) + Tara (truck) + sum(Tara(Containers))
"""

def init_config() -> List[Dict]:
    # configures and initializes MySQL database.
    
    config = {
    'user' : os.getenv("USER"),
    'password' : os.getenv("PASSWORD"),
    'host' : os.getenv("HOST"),
    'port' : os.getenv("PORT"),
    'database' : os.getenv("DATABASE")
    }
    conn = mysql.connector.connect(**config)
    cur = conn.cur()
    cur.execute('SELECT * From weighings')
    logging.debug(cur)
    cur.close()
    conn.close()
    return res

def csv_to_json(csvFile):
    # CSV to JSON parser

    data = []
    with open(csvFile) as f:
        for row in csv.DictReader(f):
            data.append(row)
    json_data = json.dumps(data)
    return json_data

@app.route('/')
def index() -> str:
    # for debugging purposes: dumps all database.
 
    return json.dumps({'weight_system': init_config()})

@app.route('/weight', methods = ['POST'])
def post_weight(jsonData):
    # Records data and server date-time and returns a json object with a unique weight.
    """
    Note that "in" & "none" will generate a new session id, and "out" will return session id of previous "in" for the truck.
    """
    data = request.get_json()  # testing
    logging.debug('printing YAY!!')  # testing
    logging.debug(data)  # testing
    return "returning YAY!!" + data  # testing

@app.route('/batch-weight', methods = ['POST'])
def post_batch_weight(jsonData):
    """
    Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers.
    """
    # File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    
    pass

@app.route('/unknown', methods = ['GET'])
def get_unknown_containers(jsonData):
    """
    Returns a list of all recorded containers that have unknown weight:
    ["id1","id2",...]
    """
    pass

@app.route('/weight', methods = ['GET'])  # /weight?from=t1&to=t2&filter=f
def get_weight_from_file(jsonData):
    """
    Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers.
    File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    """
    pass

@app.route('/item', methods = ['GET'])  # /item/<id>?from=t1&to=t2
def get_item(jsonData):
    """
    - id is for an item (truck or container). 404 will be returned if non-existent
    - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
    default t1 is "1st of month at 000000". default t2 is "now".
    """

@app.route('/session', methods = ['GET'])  # /session/<id>
def get_session_id(jsonData):
    """
    id is for a weighing session. 404 will be returned if non-existent.
    """
    pass

@app.route('/health', methods = ['GET'])
def health(jsonData):
    """
    health function...
    """
    # test acess to database
    # test read from /in directory
    # other tests...
    return "ok"
    pass


if __name__ == '__main__':
# Use interact() function to start the Interpreter with local namespace
    code.interact(banner="Start", local=locals(), exitmsg="End")
# Trigger Python Debugging Program
    pdb.set_trace()
    app.run(host='0.0.0.0', debug=True, port=5000)
