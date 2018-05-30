#/usr/bin/env python

from cloudrun.run import Run
import os

# Secret token
token = os.environ['CLOUDRUN_API_TOKEN']
url = 'https://api.cloudrun.co/v1'
userid = '8d3eee40-1700-11e7-9970-f584c576605b'

run = Run(url, token + '|' + userid)
run.create('wrf', '3.9.1')

# Upload input files
for input_file in ['namelist.input', 'wrfinput_d01', 'wrfbdy_d01']:
    run.upload(input_file)

# Start the run using 4 parallel cores
#run.start(cores=4)
