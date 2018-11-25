from typing import List, Dict
from flask import Flask
import mysql.connector
import json

app = Flask(__name__)




def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'flaskApp'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM truck')
    #print(cursor)
    results = [{truckId: providerId} for (truckId, providerId) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    print("HI EVERY BODY")
    return json.dumps({'FlaskApp': favorite_colors()})


@app.route('/health')
def index() -> str:
    return "ok"



if __name__ == '__main__':
    print("Hi Bro")
    app.run(host='0.0.0.0',debug=True)
