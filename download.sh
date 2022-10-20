#!/bin/bash

# This script can download raw PROCAR.gz files from Nomad

mkdir files
cd files
curl "http://nomad-lab.eu/prod/rae/api/archive/download?upload_id=EIDyjluDQ3eZnt-gI7Fc4Q&file_pattern=PROCAR.gz" --output nomad.zip
unzip nomad.zip