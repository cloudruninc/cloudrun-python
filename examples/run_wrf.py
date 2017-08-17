#/usr/bin/env python

from cloudrun import Cloudrun
import os

# Secret token
token = os.environ['CLOUDRUN_API_TOKEN']

# Create API session instance
api = Cloudrun(token)

# Create a new WRF run instance
run = api.create_run(model='wrf',version='3.9')



