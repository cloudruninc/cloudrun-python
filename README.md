# cloudrun-python

[![Build Status](https://travis-ci.org/cloudruninc/cloudrun-python.svg?branch=master)](https://travis-ci.org/cloudruninc/cloudrun-python)
[![GitHub issues](https://img.shields.io/github/issues/cloudruninc/cloudrun-python.svg)](https://github.com/cloudruninc/cloudrun-python/issues)

Python interface to [Cloudrun API](http://docs.cloudrun.co).

## Getting started

To install, type:

```
pip install git+https://github.com/cloudruninc/cloudrun-python
```

Example usage:

```python
from cloudrun import Cloudrun

# API session instance
api = Cloudrun(token)

# create the model run instance
run = api.create_run(model='wrf',version='3.9')

# upload input files
for input file in ['namelist.input','wrfinput_d01','wrfbdy_d01']:
    run.upload(input_file)

# start the run
run.setup()

# update run data
run.get()
```

## Documentation

Full API documentation is available [here](http://docs.cloudrun.co).

## Questions?

Need help integrating Cloudrun with your app or workflow?
[Let us know](mailto:hello@cloudrun.co)!
