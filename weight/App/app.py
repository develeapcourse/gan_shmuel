# -*-coding:utf-8 -*
from typing import List, Dict
from flask import Flask, jsonify
import mysql.connector
import json

app = Flask(__name__)

def init_config() -> List[Dict]
	config = {
	'user' : 'root',
	'password' : 'root',
	'host' : 'db',
	'port' : '3306',
	'database' : 'weight_system'
	}
	conn = mysql.connector.connect(**config)
	cur = conn.cur()
	cur.execute('SELECT * From truck')
	print(cur)
	cur.close()
	conn.close()

	return res

@app.route('/')
  def index() -> str:
	return json.dumps({'weight_system': init_config()})

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True,port=3306
