import mysql.connector
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

================
def insert_weight(session_id, date_time, weight, unit, direction, truck_id, container_id, produce ):

	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	add_weight = ("INSERT INTO weighings "
               "(session_id, date_time, weight, unit, direction, truck_id, container_id, produce) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

	# Insert new weight
	cursor.execute(add_weight, data_weight)
	# *if needed? or already initilaized*  weight_no = cursor.lastrowid

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

        bot_logger.logger.info("Save weight for session=%s, date=%s, weight=%s, unit=%s, direction=%s, truck=%s,  container/s=%s, produce=%s" % (session_id, date_time, weight, unit, direction,  truck_id, container_id, produce))
================


================
def insert_tara_container(container_id, container_weight, unit):

	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	add_tara_container = ("INSERT INTO tara_containers "
               "(container_id, container_weight, unit) "
               "VALUES (%s, %s, %s)")

	# Insert new weight
	cursor.execute(add_tara_container, data_container)
	# *if needed? or already initilaized*  container_no = cursor.lastrowid

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

        bot_logger.logger.info("Save weight for containerId=%s, weight=%s, units=%s, date=%s" % (containerId, weight, units, date))
================


================
def insert_tara_truck(truck_id, truck_weight, unit):

	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	add_tara_track = ("INSERT INTO tara_trucks "
               "(truck_id, truck_weight, unit) "
               "VALUES (%s, %s, %s)")

	# Insert new weight
	cursor.execute(add_tara_truck, data_truck)
	# *if needed? or already initilaized*  truck_no = cursor.lastrowid

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

        bot_logger.logger.info("Save weight for truck_id=%s, truck_weight=%s, unit=%s" % (truck_id, truck_weight, unit))
================


================
def get_unknown_weight_containers():
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT container_id FROM tara_containers "
         	"WHERE weight==NULL")
	cursor.execute(query)

	"""
	return as json with list of containerId 
		-for (containerId) in cursor:
 			print("container %s" % containerId)
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send containers that have unknown weight")
================


================
def get_session_by_time(fromTime, toTime, direction):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT session_id, date_time, weight, unit, direction, truck_id, container_id produce  "
                 "FROM weighings "
         	 "WHERE direction==%s and "
		 "date_time BETWEEN %s and %s ")
	cursor.execute(query, (direction, fromTime, toTime))

	"""
	return as json with list of  json objects, one per weighing (batch NOT included)
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send sessions list with details")

"""
[{ "id": <id>,
   "direction": in/out/none,
   "bruto": <int>, //in kg
   "neto": <int> or "na" // na if some of containers have unknown tara
   "produce": <str>,
   "containers": [ id1, id2, ...]
},...]
"""
================


================	
def get_tara_container(containerId ,fromTime, toTime):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT container_id, container_weight, unit, date_time "
                 "FROM tara_containers "
         	 "WHERE container_id==%s and "
		 "date_time BETWEEN %s and %s ")
	cursor.execute(query, (containerId, fromTime, toTime))

	"""
	return as json with list of containers  or 404 if not found
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send containers in some time range")
================


================
def get_tara_truck(truck_id ,fromTime, toTime):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT truck_id, weight, unit, date_time "
                 "FROM weighings "
         	 "WHERE truck_id==%s and "
		 "date_time BETWEEN %s and %s ")
	cursor.execute(query, (truck_id, fromTime, toTime))

	"""
	return as json with list of tracks or 404 if not found
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send tracks in some time range")
================


================
def get_session_weight(sessionId):
	cnx = mysql.connector.connect(user='root', database='weight_system')
	cursor = cnx.cursor()

	query = ("SELECT session_id, direction, date_time, truck_id, weight, unit, container_id,  "
                 "FROM weighings "
         	 "WHERE session_id==%s")
	cursor.execute(query, sessionId)

	"""
	return as json with specific session details or 404 if not found
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send specific session details")

 """
 { "id": <str>, 
   "truck": <truck-id> or "na",
   "bruto": <int>,
   ONLY for OUT:
   "truckTara": <int>,
   "neto": <int> or "na" // na if some of containers unknown
 }
"""
================





