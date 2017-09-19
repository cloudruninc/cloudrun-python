#/usr/bin/env python

from cloudrun import Cloudrun
from datetime import datetime
import numpy as np
import os

id = 'ead622aa054040d39c8fd741d19993f0'

# Secret token
token = os.environ['CLOUDRUN_API_TOKEN']

# Create API session instance
api = Cloudrun(token)

# Create a new WRF run instance
run = api.get_run(id)

field,time,u10 = run.read_output('u10',time1=datetime(2016,12,25,12))
field,time,v10 = run.read_output('v10',time1=datetime(2016,12,25,12))

wspd = np.sqrt(u10**2+v10**2)

print('Maximum wind speed on '
    +time[0].strftime('%Y-%m-%d %H:%M:%S')+':',np.max(wspd))
