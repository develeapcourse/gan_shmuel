from typing import List, Dict
from flask import Flask, request, send_from_directory
import mysql.connector
import json
import logging
import urlparse



app = Flask(__name__, static_url_path='')


databaseConfig = {
        'user': 'root',
        'password': 'root',
        'host': 'billingservicedb',
        'port': '3306',
        'database': 'flaskApp'
    }


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

    

@app.route('/provider/<id>', methods=["POST"])
def providerUpdate(id):
    try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('UPDATE provider SET providerName = "{0}" WHERE providerId = {1}'.format(request.form["providerName"], id))
        connection.commit()
        cursor.close()
        connection.close()
        return "ok"
    except Exception as e: 
        return(str(e))
    

@app.route('/provider', methods=["POST"])
def providerinsert():
    try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('Insert into provider VALUES (NULL, "{0}")'.format(request.form["providerName"]))
        connection.commit()
        cursor.close()
        connection.close()
        return "ok"
    except Exception as e: 
        return(str(e))


@app.route('/truck/<id>?<path>')
def getTruck(id):
    url = 'http://example.com/?q=abc&p=123'
    par = urlparse.parse_qs(urlparse.urlparse(url).query)

    return str(par)
    try:
        r = requests.get('http://service_app_weight:5000/item/{0}'.format(id))
        return r.json()
    except Exception as e:
        return str(e)


@app.route('/truckList')
def truckList():
    connection = mysql.connector.connect(**databaseConfig)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM truck')
    results = [{truckId: providerId} for (truckId, providerId) in cursor]
    cursor.close()
    connection.close()
    return str(results)

    
@app.route('/truck/<id>', methods=["POST"])
def truckUpdate(id):
    try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('UPDATE truck SET providerId = "{0}" WHERE truckId = {1}'.format(request.form["providerId"], id))
        connection.commit()
        cursor.close()
        connection.close()
        return "ok"
    except Exception as e: 
        return(str(e))
    

    
@app.route('/rates', methods=["POST"])
def uploadRates():
    filename = request.form["file"]
    print('Beginning file download with wget module')
    url = 'in/rates.csv'  
    wget.download(url, '/Users/scott/Downloads/cat4.jpg')  
    return "OK"


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
