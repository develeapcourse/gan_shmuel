"""
Weight Application
------------------
  The industrial weight is in charge of weighing trucks, allowing payment to providers.
  The WeightApp tracks all weights and allows payment to be for net weight.
  Reminder: Bruto = Neto (fruit) + Tara (truck) + sum(Tara(Containers))
"""

# -*-coding:utf-8 -*
from dotenv import load_dotenv
from flask import Flask, request, json, jsonify
from pathlib import Path
from typing import List, Dict
import ast
import mySQL_DAL
import csv
import datetime
import logging
import mysql.connector
import os
import uuid
import json
import datetime
from time import gmtime, strftime

app = Flask(__name__)

# Logging default level is WARNING (30), So switch to level DEBUG (10)
logging.basicConfig(filename = 'weight_service.log', level = logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

# Setting .env path and loading its values
load_dotenv(verbose=True)

# configures and initializes MySQL database.
config = {
'user' : os.getenv('USER'),
'password' : os.getenv('PASSWORD'),
'host' : os.getenv('HOST'),
'port' : os.getenv('PORT'),
'database' : os.getenv('DATABASE')
}

def get_new_unique_id(output_as = 'str'):
   """
   Returns a new unique id as a string, or (if passed argument 'int') as an integer.

   """
   unique_id = abs(hash(datetime.datetime.now()))
   if output_as.lower() == 'int':
       return unique_id
   return str(unique_id)

def swap_datetime_format(input_date):
    """
    Switches between input_date formats:
     - String of 14 digits:   "20180720133702"
     - Class datetime object: datetime.datetime(2018, 7, 20, 13, 37, 2, 409513)
    """
    if isinstance(input_date, datetime.datetime):
        output_date = input_date.strftime('%Y%m%d%H%M%S')
    elif isinstance(input_date, str) and len(input_date) == 14:
        output_date = datetime.datetime.strptime(input_date, '%Y%m%d%H%M%S')
    else:
        logging.error('Illegal input passed to function format_datetime.')
    return output_date

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
def index():
    return 'Weight application - please refer to spec. file for API instructions.'

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
    # getting input
    direction = request.form['direction']
    truck_id = request.form['truck']
    container_ids = request.form['containers']
    weight = request.form['weight']
    unit = request.form['unit']
    force = request.form['force']
    produce = request.form['produce']

    # reformatting input
    direction = direction.lower().strip('"').strip('\'')
    truck_id = truck_id.lower().strip('"').strip('\'')
    unit = unit.lower().strip('"').strip('\'')
    force = force.lower().strip('"').strip('\'')
    produce = produce.lower().strip('"').strip('\'')
    if force == "true":
        force = True
    elif force == "false":
        force = False
    else:
        logging.error('Post weight function recieved illegal value for key `force`: "{}"'.format(force))

    # set/get unique id
    if direction == 'in' or direction == 'none':
        session_id = get_new_unique_id()
    elif direction == 'out':
        pass
        session_id = mySQL_DAL.get_last_session_id_of_truck_entrance(truck_id)
    else:
        logging.error('Post weight function recieved illegal value for key `direction`: "{}"'.format(direction))
    return session_id # DEBUG

    # set date_time
    date_time = swap_datetime_format(datetime.datetime.now())

    # post values to db
    if mySQL_DAL.insert_weight(session_id, date_time, weight, unit, direction, truck_id, container_ids, produce, force):
        return 'success!'
    else:
        return 'something went wrong...'
    return direction  + ' ' + truck_id  + ' ' + container_ids  + ' ' + weight  + ' ' + unit  + ' ' + str(force)  + ' ' + produce

@app.route('/batch-weight', methods = ['POST'])
def post_batch_weight():
    """
    Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers.
    File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    """
    filename = request.form['file']

    if filename.endswith('.csv'):
        jsonData = csv_to_json(filename)
        jsonData = csv_to_json('/in/{}'.format(filename))  # returns weight as string instead of int
    elif filename.endswith('.json'):
        with open('/in/{}'.format(filename), 'r') as f:
            jsonData = str(json.load(f))
    else:
        logging.error('File passed to /batch-weight/{} of invalid format.'.format(filename))
        return 'Error: illegal filetype.'

    jsonData = ast.literal_eval(jsonData)
    for obj in jsonData:
        item_id = obj['id']
        weight = int(obj['weight'])
        unit = obj['unit']
        mySQL_DAL.insert_tara_container(item_id, weight, unit)
    return 'Read file "/in/{}" and uploaded to database.'.format(filename)

@app.route('/unknown', methods = ['GET'])
def get_unknown_containers():
    """
    Returns a list of all recorded containers that have unknown weight:
    ["id1","id2",...]
    """
    unknown_container_arr = mySQL_DAL.get_unknown_weight_containers()
    unknown_container_arr = [packed_container_id[0] for packed_container_id in ast.literal_eval(unknown_container_arr)]
    return str(unknown_container_arr)

@app.route('/weight?from=<string:t1>&to=<string:t2>&filter=<string:filter>', methods = ['GET'])
def get_weighings_from_dt(t1, t2, directions = ['in', 'out', 'none']):
    """
    - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
    - directions - comma delimited list of directions. default is "in,out,none"
    default t1 is "today at 000000". default t2 is "now".
    returns an array of json objects, one per weighing (batch NOT included):
    [{ "id": <id>,
       "direction": in/out/none,
       "bruto": <int>, //in kg
       "neto": <int> or "na" // na if some of containers have unknown tara
       "produce": <str>,
       "containers": [ id1, id2, ...]
    },...]
    """
    t1 = request.args['from']
    t2 = request.args['to']
    filt = request.arg['filter']  # variable not named filter due to existing object in python.
    
    # return array of json objects

@app.route('/item/<string:item_id>', methods = ['GET'])
def get_item(item_id):  # This doesn't belong in the function params: " item_id, t1=time.strftime('%Y%m%d%H%M%S',date(date.today().year, 1, 1)), t2=strftime('%Y%m%d%H%M%S', gmtime()) "
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

    t1 = request.args['from']
    t2 = request.args['to']

    data_tara_container = json.load(get_tara_container(item_id))
    data_tara_truck = json.load(get_tara_truck(item_id))
    data_weighings = json.load(get_session_by_time(t1,t2))

    return_data = {}
    sessions = []
    tara = ""
    if data_tara_container == []:
        if data_tara_track == []:
            return("404 not-found")
            logging.error("404 non-existent item, item-id: %s" % item_id)
        else:
            tara = data_tara_track[0]['weight'] + data_tara_track[0]['unit']
            for k,v in data_weighings.items():
                if v['track_id'] == item_id and v['date'] >= t1 and v['date'] <= t2:
                    sessions.append(v['session_id'])
    else:
          tara= data_tara_track[0]['weight'] + data_tara_track[0]['unit']
          for k,v in data_weighings:
              if v['date'] >= t1 and v['date'] <= t2:
                   for con in v['container_id']:
                       if con == item_id:
                           sessions.append(v['session_id'])
    data['id'] = item_id
    data['tara'] = tara
    data['sessions'] = sessions 
    json_data = json.dumps(return_data)

    return json.dumps(json_data)

@app.route('/session/<id>', methods = ['GET'])
def getSession(id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM weighings WHERE session_id=%s' % id)
        rv = cursor.fetchall()
        cursor.close()
        logging.info("fetched session info")
        if str(len(rv)) == "0":
            logging.warning("Session is Empty")
            return 'Session is Empty'
        else:
            payload = []
            content = {}
            for result in rv:
                if result[5] == 'in' or result[5] == 'none':
                    content = {'id': result[1], 'truck': result[6], 'bruto': result[3]}
                    payload.append(content)
                    content = {}
                elif result[5] == 'out':
                    cursor = connection.cursor()
                    cursor.execute('SELECT truck_weight FROM tara_trucks WHERE truck_id="%s"' % result[6])
                    taratruck = cursor.fetchone()
                    cursor.close()
                    containerslist = ast.literal_eval(result[7])
                    na_counter = 0
                    sum_containers = 0
                    for container in containerslist:
                        container = str(container)
                        cursor = connection.cursor()
                        cursor.execute('SELECT container_weight FROM tara_containers WHERE container_id="111"')#%s" % container
                        container = cursor.fetchone() 
                        cursor.close()
                        if str(container) == 'None':
                            logging.error("Container Not Found")
                            na_counter += 1
                            break
                        elif str(container[0]) == 'na':
                            logging.error("Container Found but has No Weight")
                            na_counter += 1
                            break
                        else:
                            sum_containers += int(container[0]) 
                    if na_counter == 1:   
                        content = {'id': result[1], 'truck': result[6], 'bruto': result[3], 'truckTara': str(taratruck[0]), 'neto': 'na'}
                        payload.append(content)
                        content = {}
                    elif na_counter == 0:
                        neto = int(result[3]) - (int(taratruck[0]) + sum_containers)
                        content = {'id': result[1], 'truck': result[6], 'bruto': result[3], 'truckTara': str(taratruck[0]), 'neto': str(neto)}
                        payload.append(content)
                        content = {}
                    else:
                        logging.error("BUG found in containers_weight")
                        return "Error Found in Container Weighting"
                else:
                    logging.error("Session Does not Exist")
                    return 'Session Not Found'
            return jsonify(payload)     
        connection.close()
    except Exception as e:
        logging.error("Error: DB Down")
        return str(e)
  
@app.route('/health', methods = ['GET'])
def health():
    """
    health function tests various components of service, if all are well it will return ok.
    """
    # write to log
    try:
        logging.info('Health check!')
    except Exception as e:
        return 'Error writing to log: %s' % e
    # test db connection
    try:
        cnx = mysql.connector.connect(**mySQL_DAL.databaseConfig)
        cnx.close()
    except Exception as e:
        logging.error('Database Connection Failed with Error %s' % e)
        return 'Error connected to database: %s' % e

    # test existence of /in dir
    try:
        path = '../in'
        if os.path.isdir(path) and os.path.islink(path):
            pass
    except Exception as e:
        logging.error('`/in` Directory doesn\'t exist.')
        return 'Error: %s' % e

    return 'ok'

if __name__ == '__main__':
    logging.info('Starting Flask server...')
    app.run(host='0.0.0.0', debug=True, port=5000)
