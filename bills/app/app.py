from typing import List, Dict
from flask import Flask, request
import mysql.connector
import json
import logging



app = Flask(__name__)


databaseConfig = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'flaskApp'
    }


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
        cursor.execute('UPDATE provider SET providerName = "{0}" WHERE providerId = {1}'.format("newName provider", 1))
        connection.commit()
        cursor.close()
        connection.close()
        return "ok"
    except Exception as e: 
        return(e)
    

    
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
