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
def insert_weight(sessionId, date, trackId, weight, units, containerId, direction):

	cnx = mysql.connector.connect(user='someUser', database='weights')
	cursor = cnx.cursor()

	add_weight = ("INSERT INTO weights "
               "(sessionId, date, trackId, weight, units, containerId, direction) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")

	# Insert new weight
	cursor.execute(add_weight, data_weight)
	# *if needed? or already initilaized*  weight_no = cursor.lastrowid

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

        bot_logger.logger.info("Save weight for session=%s, date=%s, track=%s, weight=%s, units=%s container/s=%s, direction=%s" % (sessionId, date, trackId, weight, units, containerId, direction))
================


================
def insert_tara_container(containerId, weight, units, date):

	cnx = mysql.connector.connect(user='someUser', database='containers')
	cursor = cnx.cursor()

	add_tara_container = ("INSERT INTO containers "
               "(containerId, weight, units, date) "
               "VALUES (%s, %s, %s, %s)")

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
def insert_tara_track(trackId, weight, units, date):

	cnx = mysql.connector.connect(user='someUser', database='tracks')
	cursor = cnx.cursor()

	add_tara_track = ("INSERT INTO tracks "
               "(trackId, weight, units, date) "
               "VALUES (%s, %s, %s, %s)")

	# Insert new weight
	cursor.execute(add_tara_track, data_track)
	# *if needed? or already initilaized*  track_no = cursor.lastrowid

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

        bot_logger.logger.info("Save weight for trackId=%s, weight=%s, units=%s, date=%s" % (containerId, weight, units, date))
================


================
def get_unknown_weight_containers():
	cnx = mysql.connector.connect(user='someUser', database='containers')
	cursor = cnx.cursor()

	query = ("SELECT containerId FROM containers "
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
	cnx = mysql.connector.connect(user='someUser', database='weights')
	cursor = cnx.cursor()

	query = ("SELECT sessionId, direction, date, trackId, weight, units, containerId,  "
                 "FROM containers "
         	 "WHERE direction==%s and "
		 "date BETWEEN %s and %s ")
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
	cnx = mysql.connector.connect(user='someUser', database='containers')
	cursor = cnx.cursor()

	query = ("SELECT containerId, weight, units, date  "
                 "FROM containers "
         	 "WHERE containerId==%s and "
		 "date BETWEEN %s and %s ")
	cursor.execute(query, (containerId, fromTime, toTime))

	"""
	return as json with list of containers  or 404 if not found
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send containers in some time range")
================


================
def get_tara_track(trackId ,fromTime, toTime):
	cnx = mysql.connector.connect(user='someUser', database='tracks')
	cursor = cnx.cursor()

	query = ("SELECT trackId, weight, units, date  "
                 "FROM tracks "
         	 "WHERE trackId==%s and "
		 "date BETWEEN %s and %s ")
	cursor.execute(query, (trackId, fromTime, toTime))

	"""
	return as json with list of tracks or 404 if not found
	"""
	cursor.close()
	cnx.close()

        bot_logger.logger.info("send tracks in some time range")
================


================
def get_session_weight(sessionId):
	cnx = mysql.connector.connect(user='someUser', database='weights')
	cursor = cnx.cursor()

	query = ("SELECT sessionId, direction, date, trackId, weight, units, containerId,  "
                 "FROM weights "
         	 "WHERE sessionId==%s")
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





