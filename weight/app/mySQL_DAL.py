# -*-coding:utf-8 -*
from dotenv import load_dotenv
import json
import logging
import mysql.connector
import os

# Logging default level is WARNING (30), So switch to level DEBUG (10)
logging.basicConfig(filename = 'weight_service.log', level = logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

# Setting .env path and loading its values
load_dotenv(verbose=True)

# database connection configuration and credentials:
databaseConfig = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'database': os.getenv('DATABASE')
}


def insert_weight(session_id, date_time, weight, unit, direction, truck_id, container_id, produce, force):
    try:
        # init connection to db
        cnx = mysql.connector.connect(**databaseConfig)
        cursor = cnx.cursor()

    # TODO: check if force and handle appropriatley

    # Insert new weight
        add_weight = ('INSERT INTO weighings (session_id, datetime, weight, unit, direction, truck_id, container_id, produce) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
        data_weight = (session_id, date_time, weight, unit, direction, truck_id, container_id, produce)
        cursor.execute(add_weight, data_weight)
        cnx.commit()
        logging.info('Saved weight for session=%s, date=%s, weight=%s, unit=%s, direction=%s, truck=%s,  container/s=%s, produce=%s' % (session_id, date_time, weight, unit, direction,  truck_id, container_id, produce))

    # cleanup
        cursor.close()
        cnx.close()

        return True  # On success
    except Exception as e:
        logging.error("Error: insert_weight could not process")
        return str(e)

def insert_tara_container(container_id, container_weight, unit):
    try:
        # init connection to db
        cnx = mysql.connector.connect(**databaseConfig)
        cursor = cnx.cursor()

        # Insert new weight
        add_tara_container = ('INSERT INTO  tara_containers (container_id, container_weight, unit) VALUES (%s, %s, %s)')
        values  = (container_id, container_weight, unit)
        cursor.execute(add_tara_container, values)
        cnx.commit()
        #logging.info('Save weight for container_id=%s, weight=%s, unit=%s, date=%s' % (container_id, weight, unit))

        # cleanup
        cursor.close()
        cnx.close()
    except Exception as e:
        logging.error("Error: DB Down")
        return str(e)


def insert_tara_truck(truck_id, truck_weight, unit):
    try:
        # init connection to db
        cnx = mysql.connector.connect(**databaseConfig)
        cursor = cnx.cursor()

        # Insert new weight
        add_tara_track = ('INSERT INTO tara_trucks (truck_id, truck_weight, unit) VALUES (%s, %s, %s)')
        cursor.execute(add_tara_truck, data_truck)
        cnx.commit()
        logging.info('Save weight for truck_id=%s, truck_weight=%s, unit=%s' % (truck_id, truck_weight, unit))

        # cleanup
        cursor.close()
        cnx.close()
    except Exception as e:
        logging.error("Error: DB Down")
        return str(e)

def get_unknown_weight_containers():
    # init connection to db
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    # querying db
    query = ('SELECT container_id FROM tara_containers WHERE container_weight IS NULL')
    cursor.execute(query)
    rv = cursor.fetchall()
    logging.info('send containers that have unknown weight')

    # cleanup
    cursor.close()
    cnx.close()

    return str(rv)

def get_session_by_time(fromTime, toTime):
    # init connection to db
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    # querying db
    query = ('SELECT * FROM weighings WHERE date_time BETWEEN %s and %s')
    cursor.execute(query, (fromTime, toTime))
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    logging.info('send sessions list with details')

    # cleanup
    cursor.close()
    cnx.close()

    return json.dumps(json_data)

def get_tara_container(containerId):
    # init connection to db
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    # querying db
    query = ('SELECT * FROM tara_containers WHERE container_id=%s')
    cursor.execute(query, (containerId))
    row_headers = [x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    logging.info('send specific container')

    # cleanup
    cursor.close()
    cnx.close()

    return json.dumps(json_data)

def get_tara_truck(truck_id):
    # init connection to db
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    # querying db
    query = ('SELECT * FROM weighings WHERE truck_id=%s')
    cursor.execute(query, (truck_id))
    row_headers = [x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    logging.info('send specific track')

    # cleanup
    cursor.close()
    cnx.close()

    return json.dumps(json_data)

def get_session_weight(sessionId):
    # init connection to db
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    # querying db
    query = ('SELECT * FROM weighings WHERE session_id=%s')
    cursor.execute(query, sessionId)
    row_headers = [x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    logging.info('send specific session details')

    # cleanup
    cursor.close()
    cnx.close()

    return json.dumps(json_data)

