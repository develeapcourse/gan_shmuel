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
from os.path import isdir, islink
from pathlib import Path
from typing import List, Dict
import ast
import mySQL_DAL
import csv
import datetime
import logging
import mysql.connector
import uuid
import json
import datetime
from time import gmtime, strftime
import os

# Logging default level is WARNING (30), So switch to level DEBUG (10)
logging.basicConfig(filename = 'weight_service.log', level = logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

# make flask instance of our app
app = Flask(__name__)


# database connection configuration and credentials:
databaseConfig = {
    'user': os.getenv('USER', default = 'root'),
    'password': os.getenv('PASSWORD', default = 'root'),
    'host': os.getenv('HOST', default = 'service_db_weight'),
    'port': os.getenv('PORT', default = '3306'),
    'database': os.getenv('DATABASE', default = 'weight_system')
}




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
    direction = request.form['direction']
    truck_id = request.form['truck']
    container_ids = request.form['containers']
    weight = request.form['weight']
    unit = request.form['unit']
    force = request.form['force']
    produce = request.form['produce']
    # post values to db

    # return json on success
    pass  # temporary line, until function and return implemented

@app.route('/batch-weight', methods = ['POST'])
def post_batch_weight():
    """
    Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers.
    File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
    """
    filename = request.form['file']

    if filename.endswith('.csv'):
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
    returns an array of json objects, one per weighing (batch NOT included)
    """
    t1 = request.args['from']
    t2 = request.args['to']
    filt = request.arg['filter']  # variable not named filter due to existing object in python.
    
    # return array of json objects

@app.route('/item/<string:item_id>', methods = ['GET'])
def get_item(item_id):
  # This doesn't belong in the function params: " item_id, t1=time.strftime('%Y%m%d%H%M%S',date(date.today().year, 1, 1)), t2=strftime('%Y%m%d%H%M%S', gmtime()) "
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
   
    """
    data_tara_container = json.load(mySQL_DAL.get_tara_container(item_id))
    logging.info("data tara is: %s" % data_tara_container)
    data_tara_truck = json.load(mySQL_DAL.get_tara_truck(item_id))
    data_weighings = json.load(mySQL_DAL.get_session_by_time(t1,t2))
    return data_tara_container
    """    
    sessions = []
    tara = ""
       
    #========DAL to tara_container
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()
    #quering db
    query = ("SELECT * FROM tara_containers WHERE container_id=%s" % item_id)
    cursor.execute(query)
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    item_data = []
    for result in rv:
        item_data.append(dict(zip(row_headers,result)))
    logging.info('send specific container and data is: %s' % rv)
    # cleanup
    cursor.close()
    cnx.close()
    query=""
    logging.info("item data is: %s and json dumps is: %s" % (item_data, json.dumps(item_data)))
    if item_data == []:
         #======DAL to tara_tracks - to check if item is from tracks table
         cnx = mysql.connector.connect(**databaseConfig)
         cursor = cnx.cursor()
         #quering db
         query = ("SELECT * FROM tara_tracks WHERE track_id=%s" % item_id)
         cursor.execute(query)
         row_headers=[x[0] for x in cursor.description] #this will extract row headers
         rv = cursor.fetchall()
         logging.info("data: %s" % rv)
         item_data = []
         for result in rv:
                item_data.append(dict(zip(row_headers,result)))
         # cleanup
         cursor.close()
         cnx.close()
         query=""
         logging.info("item data is: %s and json dumps is: %s" % (item_data, json.dumps(item_data)))
         if item_data == []:
             logging.error("404 non-existent item, item-id: %s" % item_id)
             return "404 not found"
         else:
             #========DAL to weighings to check the sessions id's
             query = ("SELECT * FROM weighings WHERE track_id=%s" % item_id)
    else:  
         #========DAL to weighings to check the sessions id's
         query = ("SELECT * FROM weighings w WHERE FIND_IN_SET(%s, w.containers)" % item_id)
    
    if query != "":
         #========DAL to weighings to check the sessions id's
         cnx = mysql.connector.connect(**databaseConfig)
         cursor = cnx.cursor()
         #quering db
         cursor.execute(query)
         row_headers=[x[0] for x in cursor.description] #this will extract row headers
         rv = cursor.fetchall()
         session_data = []
         for result in rv:
              session_data.append(dict(zip(row_headers,result)))
         logging.info('data is: %s' % rv)
         # cleanup
         cursor.close()
         cnx.close()


         logging.info("instance found in tara container")
         
    """
    if data_tara_container == []:
        #if data_tara_track == []:
       
           # logging.error("404 non-existent item, item-id: %s" % item_id)
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
    """
@app.route('/session/<string:session_id>', methods = ['GET'])
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
    sessionInfos = []
    try:
        connection = mysql.connector.connect(**mySQL_DAL.databaseConfig)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM weighings WHERE session_id=%s' % session_id)
        sessionInfos=cursor.fetchall()
        print("coucou")
    except Exception as e:
        logging.error('Request failed with error: %s' % e)
        return 'Error: %s' % e
    # return json

@app.route('/health', methods = ['GET'])
def health():
    """
    health function tests various components of service, if all are well it will return ok.
    """
    # test db connection
    try:
        cnx = mysql.connector.connect(**mySQL_DAL.databaseConfig)
        cnx.close()
    except Exception as e:
        logging.error('Database connection failed with error %s' % e)
        return 'Error: %s' % e

    # test existence of /in dir
    try:
        path = '../in'
        if isdir(path) and islink(path):
            pass
    except Exception as e:
        logging.error('`/in` directory doesn\'t exist.')
        return 'Error: %s' % e

    return 'ok'

if __name__ == '__main__':
    logging.info('Starting Flask server...')
    app.run(host='0.0.0.0', debug=True, port=5000)
