#!/bin/bash

bills_path="bills"
weight_path="weight"
devops_path="devops"

docker_compose_destinations='-f '$bills_path'/docker-compose.yml -f '$weight_path'/docker-compose.yml -f '$devops_path'/docker-compose.override.yml'

docker-compose $docker_compose_destinations up -d
