#!/bin/bash
docker-compose run nomad-web django-admin process_xml --source_id 1
docker-compose run nomad-web django-admin process_xml --source_id 2
