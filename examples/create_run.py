#!/usr/bin/env python

from cloudrun import Api
from datetime import datetime, timedelta
import os

token = os.environ['CLOUDRUN_API_TOKEN']
userid = '8d3eee40-1700-11e7-9970-f584c576605b'
url = 'https://api.cloudrun.co/v1'

api = Api(url, token + '|' + userid)

status, body = api.create_run('wrf', '3.9.1')
runid = body['id']

for filename in ['namelist.input', 'wrfinput_d01', 'wrfbdy_d01']:
    status, body = api.upload_file(runid, filename)

status, body = api.get_run(runid)

print(status)
print(body)
