#!/usr/bin/python3
import requests
import json
import pytest

url_weight = "http://localhost:6002"
url_bills = "http://localhost:6001"
provider_name = '@#ASD!DNF20947ASDM_test'
truck_plate = "47298743h(@*#FJASDH098234h"
provider_id=""



def test_get_health():
	global url_bills
	global url_weight
	global r_weight
	global r_bills
	assert requests.get(url_weight)
	assert requests.get(url_bills)
	r_bills = requests.get(url_bills)
	r_weight = requests.get(url_weight)
	
# basic health tests
def test_health1():
	assert r_weight.status_code == 200

def test_health2():
	assert r_bills.status_code == 200

################ weight tests ################

# def test_post_weight():
# 	payload = {
# 		'direction' : 'in',
# 		'truck' : '47298743h(@*#FJASDH098234h',
# 		'containers' : ''
# 	}
# 	r = requests.post(url=url_weight+"/weight", data=payload)
# 	assert r.status_code == 200








################ bills tests #################
@pytest.fixture
def get_prov_id():
	payload = {'providerName' : provider_name }
	global provider_id
	provider_id = requests.post(url=url_bills+"/provider", data=payload)


# post tests
def test_post_provider(get_prov_id):
	assert provider_id.status_code == 200
	assert provider_id.text.find(provider_name) is not -1
	parsed_json = json.loads(str(provider_id.text))
	assert parsed_json[provider_id] == provider_name

def test_post_rates():
	payload = {'file' : 'test.xlsx'}
	r = requests.post(url=url_bills+"/rates", data=payload)
	assert r.status_code == 200

def test_post_truck():
	payload = {'provider' : provider_name, 'id' : truck_plate}
	r = requests.post(url=url_bills+"/truck", data=payload)
	assert r.status_code == 200

# get tests
def test_get_rates():
	r = requests.get(url=url_bills+"/getrates")
	assert r.status_code == 200

# add a session weight before
def test_get_truck():
	r = requests.get(url=url_bills+"/truck/"+truck_plate)
	assert r.status_code == 200


def test_get_bill(get_prov_id):
	r = requests.get(url=url_bills+"/bill/"+ provider_id)
	assert r.status_code == 200
	assert r.text.find(provider_name) is not -1
