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
       try:
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
           return json.dumps({'FlaskApp': listTruck()})
         else:
             return "This provider does not exist in the system"
       except Exception as e:
              return e


@app.route('/providerInsert', methods=["POST"])
def providerInsert():
       try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO provider VALUES (NULL, "%s")'%(request.form["providerName"]))
        #cursor.execute('INSERT INTO provider VALUES (providerId,providerName)')
        connection.commit()
        cursor.close()
        connection.close()
        return json.dumps({'FlaskApp': listProvider()})
       except Exception as e:
          return e

@app.route('/listTruck')
def listTruck() -> List[Dict]:
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
def providerList():
    connection = mysql.connector.connect(**databaseConfig)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM provider')
    results = [{providerId: providerName} for (providerId, providerName) in cursor]
    cursor.close()
    connection.close()
    return str(results)


def listProvider() -> List[Dict]:
    connection = mysql.connector.connect(**databaseConfig)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM provider')
    #print(cursor)
    results = [{providerId: providerName} for (providerId, providerName) in cursor]
    cursor.close()
    connection.close()
    return results  

@app.route('/provider/<id>', methods=["POST"])
def providerUpdate(id):
    try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('UPDATE provider SET providerName = "{0}" WHERE providerId = {1}'.format("newName provider", 1))
        connection.commit()
        cursor.close()
        connection.close()
        return "ok"
    except Exception as e: 
        return(e)

@app.route('/')
def index() -> str:
    print("HI EVERY BODY")
    return "IndexPage"


@app.route('/health')
def health()-> str:
    return "ok"

if __name__ == '__main__':
    print("Hi Bro")
    app.run(host='0.0.0.0',debug=True)

