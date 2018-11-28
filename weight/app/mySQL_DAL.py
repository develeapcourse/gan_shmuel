import json
import logging
import mysql.connector
import os


# database connection configuration and credentials:
databaseConfig = {
    'user' : os.getenv('USER', default = 'root'),
    'password' : os.getenv('PASSWORD', default = 'root'),
    'host' : os.getenv('HOST', default = 'service_db_weight'),
    'port' : os.getenv('PORT', default = '3306'),
    'database' : os.getenv('DATABASE', default = 'weight_system')
}



def insert_weight(session_id, date_time, weight, unit, direction, truck_id, container_id, produce ):

    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    add_weight = ("INSERT INTO weighings "
                  "(session_id, date_time, weight, unit, direction, truck_id, container_id, produce) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    # Insert new weight
    cursor.execute(add_weight, data_weight)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    logging.info("Saved weight for session=%s, date=%s, weight=%s, unit=%s, direction=%s, truck=%s,  container/s=%s, produce=%s" % (session_id, date_time, weight, unit, direction,  truck_id, container_id, produce))



def insert_tara_container(container_id, container_weight, unit):
    # init connection to db
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    # Insert new weight
    add_tara_container = ('INSERT INTO  tara_containers (container_id, container_weight, unit) VALUES (%s, %s, %s)')
    values  = (container_id, container_weight, unit)
    cursor.execute(add_tara_container, values)
    cnx.commit()
    #logging.info("Save weight for container_id=%s, weight=%s, unit=%s, date=%s" % (container_id, weight, unit))

    # cleanup
    cursor.close()
    cnx.close()


def insert_tara_truck(truck_id, truck_weight, unit):

    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    add_tara_track = ("INSERT INTO tara_trucks "
                      "(truck_id, truck_weight, unit) "
                      "VALUES (%s, %s, %s)")

    # Insert new weight
    cursor.execute(add_tara_truck, data_truck)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    logging.info("Save weight for truck_id=%s, truck_weight=%s, unit=%s" % (truck_id, truck_weight, unit))

def get_unknown_weight_containers():
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    query = ('SELECT container_id FROM tara_containers WHERE container_weight IS NULL')
    cursor.execute(query)
    rv = cursor.fetchall()
    return str(rv)
    cursor.close()
    cnx.close()
    logging.info("send containers that have unknown weight")

    return jsonify(payload)

def get_session_by_time(fromTime, toTime):
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    query = ("SELECT *  "
             "FROM weighings "
             "WHERE date_time BETWEEN %s and %s ")
    cursor.execute(query, (fromTime, toTime))
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    cnx.close()
    logging.info("send sessions list with details")

    return json.dumps(json_data)


"""
[{ "id": <id>,
   "direction": in/out/none,
   "bruto": <int>, //in kg
   "neto": <int> or "na" // na if some of containers have unknown tara
   "produce": <str>,
   "containers": [ id1, id2, ...]
},...]
"""

def get_tara_container(containerId):
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    query = ("SELECT * "
             "FROM tara_containers "
             "WHERE container_id=%s")
    cursor.execute(query, (containerId))
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    cnx.close()
    logging.info("send specific container")
    return json.dumps(json_data)

def get_tara_truck(truck_id):
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    query = ("SELECT * "
             "FROM weighings "
             "WHERE truck_id=%s")
    cursor.execute(query, (truck_id))
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    cnx.close()
    logging.info("send specific track")
    return json.dumps(json_data)

def get_session_weight(sessionId):
    cnx = mysql.connector.connect(**databaseConfig)
    cursor = cnx.cursor()

    query = ("SELECT *  "
             "FROM weighings "
             "WHERE session_id=%s")
    cursor.execute(query, sessionId)
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    cnx.close()
    logging.info("send specific session details")

    return json.dumps(json_data)

