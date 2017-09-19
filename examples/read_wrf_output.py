#/usr/bin/env python

from cloudrun import Cloudrun
from datetime import datetime
import numpy as np
import os

# Secret token
token = os.environ['CLOUDRUN_API_TOKEN']

# Create API session instance
api = Cloudrun(token)

# Access an existing WRF run
run = api.get_run('ead622aa054040d39c8fd741d19993f0')

# Read 10-m u wind on 2016-12-25 12:00 UTC
field,time,u10 = run.read_output('u10',time1=datetime(2016,12,25,12))

# Read 10-m v wind on 2016-12-25 12:00 UTC
field,time,v10 = run.read_output('v10',time1=datetime(2016,12,25,12))

# Calculate wind speed from components
wspd = np.sqrt(u10**2+v10**2)

print('Maximum wind speed on '
    +time[0].strftime('%Y-%m-%d %H:%M:%S')+':',np.max(wspd))
