from typing import List, Dict
from flask import Flask, request, send_from_directory
import mysql.connector
import openpyxl as xl
import json
import requests
import logging

from datetime import datetime
app = Flask(__name__, static_url_path='')

databaseConfig = {
        'user': 'root',
        'password': 'root',
        'host': 'billingservicedb',
        'port': '3306',
        'database': 'flaskApp'
    }

@app.route('/truck', methods=["POST"])
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
             return  str(e)
           cursor.close()
           connection.close()
           return json.dumps({'FlaskApp': listTruck()})
         else:
             return "This provider does not exist in the system"
       except Exception as e:
              return str(e)


@app.route('/provider', methods=["POST"])
def providerInsert():
       try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO provider VALUES (NULL, "%s")'%(request.form["providerName"]))
        connection.commit()
        cursor.close()
        connection.close()
        return json.dumps({'FlaskApp': listProvider()})
       except Exception as e:
          return str(e)

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
        return send_from_directory('in', "rates.xlsx")
    except Exception as e:
        return str(e)


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
    results = [{providerId: providerName} for (providerId, providerName) in cursor]
    cursor.close()
    connection.close()
    return results  


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
    

@app.route('/truck/<id>', methods=["GET"])
def get_truck(id):

    date_from = request.args.get("from")
    date_to = request.args.get("to")

    # Checking the dateFrom validity
    if date_from is None:
        # By default the date_from is from the first day of the current month
        date_from = datetime.now().strftime('%Y%m01000000')
    elif re.match("^[0-9]{14}$", date_from) is None:
        return "The format of date from is not correct"

    # Checking the dateTo format
    if date_to is None:
        # By default the date_to is now
        date_to = datetime.now().strftime('%Y%m%d%H%M%S')
    elif re.match("^[0-9]{14}$", date_to) is None:
        return "The format of date to is not correct"

    try:
        response = requests.get('http://service_app_weight:5000/item/{0}?from={1}&to={2}'.format(id,date_from,date_to))
        return response.json()
    except Exception as error:
        return str(error)


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
    

@app.route("/rates",methods=["POST"])
def postrates():
    filename = request.args.get("file")

    try:
        wb = xl.load_workbook("in/" + filename )
        ws = wb.get_active_sheet()
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()
        sql_insert_rates_query = "INSERT INTO rates (productName, scope, rates) VALUES (%s, %s, %s)"
        cursor.execute('TRUNCATE TABLE rates')
        row = 2
        while ws.cell(row, 1).value is not None:
            productName = ws.cell(row, 1).value
            rate = ws.cell(row, 2).value
            scope = ws.cell(row, 3).value
            insert_tuple = (productName, scope, rate)
            cursor.execute(sql_insert_rates_query, insert_tuple)
            row += 1

        connection.commit()
        cursor.close()
        connection.close()
        return "RATES UPLOADED"
    except FileNotFoundError:
        return "File Not Found"

    except mysql.connector.Error as error:
        return "Rates uploading failed {}".format(error)

    except Exception as error:
        return "Error {}".format(error)

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

