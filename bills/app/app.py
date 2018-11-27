from typing import List, Dict
from flask import Flask, request, send_from_directory
import mysql.connector
import openpyxl as xl
import json
import logging

app = Flask(__name__, static_url_path='')


logging.basicConfig(filename = 'test.log', level = logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

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
          cursor.execute('INSERT INTO truck VALUES (%d, %d)'%((int(request.form["truckId"])),int(request.form["providerId"])))
          connection.commit()
          cursor.close()
          connection.close()
          return ('A  %d truck was added successfully'%(int(request.form["truckId"])))
       else:
         logging.error("This provider does not exist in the system")
         return ("This %d provider does not exist in the system"%(int(request.form["providerId"])))
    except Exception as e:
        logging.error("Failed to add %d provider"%(int(request.form["truckId"])))
        return e

@app.route('/provider', methods=["POST"])
def providerInsert():
       logging.info('Add new provider to the table')
       try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO provider VALUES (NULL, "%s")'%(request.form["providerName"]))
        connection.commit()
        cursor.close()
        connection.close()
        logging.info('A %s provider was added successfully'%(request.form["providerName"]))
        return json.dumps({'FlaskApp': providerList()})
       except Exception as e:
          logging.error("Failed to add truck %s"%(request.form["providerName"]))
          return str(e)

@app.route('/truckList')
def listTruck() -> List[Dict]:
    try:
     connection = mysql.connector.connect(**databaseConfig)
     cursor = connection.cursor()
     cursor.execute('SELECT * FROM truck')
     results = [{truckId: providerId} for (truckId, providerId) in cursor]
     cursor.close()
     connection.close()
     logging.info('Show all trucks successfully completed')
     return str(results)
    except Exception as e:
        logging.error("Failed to view all trucks")
        return e

@app.route('/rates')
def getRates():
    try:
        return send_from_directory('in', "rates.xlsx")
        logging.info("rates.xlsx file downloaded successfully")
    except Exception as e:
        logging.error("Failed to download file rates.xlsx")
        return str(e)


@app.route('/providerList')
def providerList() -> List[Dict]:
    try:
     connection = mysql.connector.connect(**databaseConfig)
     cursor = connection.cursor()
     cursor.execute('SELECT * FROM provider')
     results = [{providerId: providerName} for (providerId, providerName) in cursor]
     cursor.close()
     connection.close()
     logging.info('Show all providers successfully completed')
     return str(results)
    except Exception as e:
        logging.error("Failed to view all providers")
        return e

@app.route('/provider/<id>', methods=["POST"])
def providerUpdate(id):
    try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('UPDATE provider SET providerName = "{0}" WHERE providerId = {1}'.format(request.form["providerName"], id))
        connection.commit()
        cursor.close()
        connection.close()
        logging.info('%s provider Update'%id)
        return "ok"
    except Exception as e:
        logging.error("Failed to update %s provider"%id)
        return(e)


@app.route('/truckList')
def truckList():
    try:
     connection = mysql.connector.connect(**databaseConfig)
     cursor = connection.cursor()
     cursor.execute('SELECT * FROM truck')
     results = [{truckId: providerId} for (truckId, providerId) in cursor]
     cursor.close()
     connection.close()
     logging.info('Show all trucks successfully completed')
     return str(results)
    except Exception as e:
        logging.error("Failed to view all trucks")
        return e

    
@app.route('/truck/<id>', methods=["POST"])
def truckUpdate(id):
    try:
        connection = mysql.connector.connect(**databaseConfig)
        cursor = connection.cursor()  
        cursor.execute('UPDATE truck SET providerId = "{0}" WHERE truckId = {1}'.format(request.form["providerId"], id))
        connection.commit()
        cursor.close()
        connection.close()
        logging.info('%s truck Update'%id)
        return "ok"
    except Exception as e:
        logging.error("Failed to update %s provider"%id)
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
        logging.info("RATES UPLOADED")
        return "RATES UPLOADED"
    except FileNotFoundError:
        logging.error("File Not Found")
        return "File Not Found"

    except mysql.connector.Error as error:
        logging.error("Rates uploading failed {}".format(error))
        return "Rates uploading failed {}".format(error)

    except Exception as error:
        logging.error("Error {}".format(error))
        return "Error {}".format(error)

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

