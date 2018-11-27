#!/usr/bin/python3
import requests

url_weight = "http://localhost:6002"
url_bills = "http://localhost:6001"

try:
	r_weight = requests.get(url_weight)
	r_bills = requests.get(url_bills)
except Exception as e:
	print("Error:\n" + str(e))
	exit(1)


def test_health():
	assert r_weight.status_code == 200
	assert r_bills.status_code == 200


test_health()