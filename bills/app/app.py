from typing import List, Dict
from flask import Flask, request, send_from_directory
import mysql.connector
import json
import logging

app = Flask(__name__, static_url_path='')


databaseConfig = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'flaskApp'
    }

@app.route('/truckInsert', methods=["POST"])
def truckInsert():
       logging.info('Add new truck to the table')
       connection = mysql.connector.connect(**databaseConfig)
       cursor = connection.cursor()
       cursor.execute('SELECT * FROM provider WHERE providerId = %d'%(int(request.form["providerId"])))
       myProviderId = [{providerId} for (providerId) in cursor]
       if myProviderId:
        try:
          cursor.execute('INSERT INTO truck VALUES (%d, %d)'%((int(request.form["truckId"])),int(request.form["providerId"])))
          connection.commit()
        except Exception as e:
          return  e
        cursor.close()
        connection.close()
        return "aa"
       else:
             return "This provider does not exist in the system"
      # return json.dumps({'FlaskApp': listTruck()})



@app.route('/providerInsert', methods=["POST"])
def providerInsert():
       logging.info('Add new provider to the table')
       try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO provider VALUES (NULL, "%s")'%(request.form["providerName"]))
        #cursor.execute('INSERT INTO provider VALUES (providerId,providerName)')
        connection.commit()
        cursor.close()
        connection.close()
        return json.dumps({'FlaskApp': providerList()})
       except Exception as e:
          return e

@app.route('/listTruck')
def listTruck() -> List[Dict]:
    logging.info('View all trucks')
    connection = mysql.connector.connect(**databaseConfig)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM truck')
    #print(cursor)
    results = [{truckId: providerId} for (truckId, providerId) in cursor]
    cursor.close()
    connection.close()
    return str(results)

@app.route('/rates')
def getRates():
    try:
        return send_from_directory('in', "test.xlsx")
    except Exception as e:
        return e

@app.route('/providerList')
def providerList() -> List[Dict]:
    try:
     logging.info('View all providers')
     connection = mysql.connector.connect(**databaseConfig)
     cursor = connection.cursor()
     cursor.execute('SELECT * FROM provider')
     results = [{providerId: providerName} for (providerId, providerName) in cursor]
     cursor.close()
     connection.close()
     return str(results)
    except Exception as e:
        logging.error("Can't view tha all providers")
        return e

@app.route('/provider/<id>', methods=["POST"])
def providerUpdate(id):
    try:
        logging.info('Provider Update %s'%id)
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('UPDATE provider SET providerName = "{0}" WHERE providerId = {1}'.format("newName provider", 1))
        connection.commit()
        cursor.close()
        connection.close()
        return "ok"
    except Exception as e:
        logging.error("Can't update provider %s"%id)
        return(e)

@app.route('/')
def index() -> str:
    print("HI EVERY BODY")
    return "IndexPage"


@app.route('/health')
def health()-> str:
    return "ok"

if __name__ == '__main__':
    logging.info('Starting Flask server...')
    print("Hi Bro")
    app.run(host='0.0.0.0',debug=True)

