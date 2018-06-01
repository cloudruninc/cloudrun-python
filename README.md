# cloudrun-python

[![Build Status](https://travis-ci.org/cloudruninc/cloudrun-python.svg?branch=master)](https://travis-ci.org/cloudruninc/cloudrun-python)
[![GitHub issues](https://img.shields.io/github/issues/cloudruninc/cloudrun-python.svg)](https://github.com/cloudruninc/cloudrun-python/issues)

Official Python interface to [Cloudrun API](http://docs.cloudrun.co).

## Installation

```
git clone https://github.com/cloudruninc/cloudrun-python
cd cloudrun-python
pip install -U .
```

To run tests:

```
pytest -v cloudrun/tests.py
```

## Example usage

### Creating and starting a WRF run

```python
from cloudrun import Run
import os

# Secret token
token = os.environ['CLOUDRUN_API_TOKEN']
url = 'https://api.cloudrun.co/v1'

run = Run(url, token)
run.create('wrf', '3.9.1')

# Upload input files
for input_file in ['namelist.input', 'wrfinput_d01', 'wrfbdy_d01']:
    run.upload(input_file)

# Start the run using 4 parallel cores
run.start(cores=4)
```

[Contact us](mailto:accounts@cloudrun.co) to obtain an API token.

## Documentation

Full API documentation is available [here](http://docs.cloudrun.co).

## Questions?

Need help integrating Cloudrun with your app or workflow?
[Let us know](mailto:hello@cloudrun.co)!
