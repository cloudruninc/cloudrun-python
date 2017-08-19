#/usr/bin/env python

from cloudrun import Cloudrun
import os

# Secret token
token = os.environ['CLOUDRUN_API_TOKEN']

# Create API session instance
api = Cloudrun(token)

# Create a new WRF run instance
run = api.create_run(model='wrf',version='3.9')

# Upload input files
for input_file in ['namelist.input','wrfinput_d01','wrfbdy_d01']:
    print(input_file)
    run.upload(input_file)

# Start the run
run.start(cores=1)
