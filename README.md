# cloudrun-python

[![Build Status](https://travis-ci.org/cloudruninc/cloudrun-python.svg?branch=master)](https://travis-ci.org/cloudruninc/cloudrun-python)
[![GitHub issues](https://img.shields.io/github/issues/cloudruninc/cloudrun-python.svg)](https://github.com/cloudruninc/cloudrun-python/issues)

Official Python interface to [Cloudrun API](http://docs.cloudrun.co).

## Installation

```
pip install git+https://github.com/cloudruninc/cloudrun-python
```

## Example usage

### Creating and starting a WRF run

```python
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
    run.upload(input_file)

# Start the run using 4 parallel cores
run.start(cores=4) 
```

### Reading WRF output

```python
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
field,time,u10 = run.read_output('u10',time1=datetime(2016,12,25,12)
```

[Contact us](mailto:accounts@cloudrun.co) to obtain an API token.

## Documentation

Full API documentation is available [here](http://docs.cloudrun.co).

## Questions?

Need help integrating Cloudrun with your app or workflow?
[Let us know](mailto:hello@cloudrun.co)!
