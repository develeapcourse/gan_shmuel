import mysql.connector
import logging
import json
from mysql.connector import errorcode
from __future__ import print_function
from datetime import date, datetime, timedelta

"""
***try and catch to connecting to DB***
try:
  cnx = mysql.connector.connect(user='scott',
                                database='employ')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
"""


def insert_weight(session_id, date_time, weight, unit, direction, truck_id, container_id, produce ):

	cnx = mysql.connector.connect(user='root', database='weight_system')
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
        logger.info("Save weight for session=%s, date=%s, weight=%s, unit=%s, direction=%s, truck=%s,  container/s=%s, produce=%s" % (session_id, date_time, weight, unit, direction,  truck_id, container_id, produce))



def insert_tara_container(container_id, container_weight, unit):

	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	add_tara_container = ("INSERT INTO tara_containers "
               "(container_id, container_weight, unit) "
               "VALUES (%s, %s, %s)")

	# Insert new weight
	cursor.execute(add_tara_container, data_container)

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
        logger.info("Save weight for containerId=%s, weight=%s, units=%s, date=%s" % (containerId, weight, units, date))



def insert_tara_truck(truck_id, truck_weight, unit):

	cnx = mysql.connector.connect(user='root', database='weight_system')
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
        logger.info("Save weight for truck_id=%s, truck_weight=%s, unit=%s" % (truck_id, truck_weight, unit))



def get_unknown_weight_containers():
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT container_id FROM tara_containers "
         	"WHERE weight==NULL")
	cursor.execute(query)
        rv = cur.fetchall()
        payload = []
        content = {}
        for result in rv:
                 content = {result[0]}
        payload.append(content)
        content = {}
  
	cursor.close()
	cnx.close()
        logger.info("send containers that have unknown weight")
  
        return jsonify(payload)


def get_session_by_time(fromTime, toTime, direction):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT *  "
                 "FROM weighings "
         	 "WHERE direction=%s AND date_time BETWEEN %s and %s ")
	cursor.execute(query, (direction, fromTime, toTime))
	row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
     		   json_data.append(dict(zip(row_headers,result)))

	cursor.close()
	cnx.close()
        logger.info("send sessions list with details")

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

def get_tara_container(containerId ,fromTime, toTime):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT * "
                 "FROM tara_containers "
         	 "WHERE container_id=%s AND date_time BETWEEN %s and %s ")
	cursor.execute(query, (containerId, fromTime, toTime))
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
                 json_data.append(dict(zip(row_headers,result)))
 
	cursor.close()
	cnx.close()
        logger.info("send containers in some time range")
        return json.dumps(json_data)


def get_tara_truck(truck_id ,fromTime, toTime):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT * "
                 "FROM weighings "
         	 "WHERE truck_id=%s AND date_time BETWEEN %s and %s ")
	cursor.execute(query, (truck_id, fromTime, toTime))
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
                 json_data.append(dict(zip(row_headers,result)))
	
	cursor.close()
	cnx.close()
        logger.info("send tracks in some time range")
        return json.dumps(json_data)



def get_session_weight(sessionId):
	cnx = mysql.connector.connect(user='root', database='weight_system')
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
        logger.info("send specific session details")

        return json.dumps(json_data)






