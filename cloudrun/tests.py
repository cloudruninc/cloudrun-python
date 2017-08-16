import datetime
import json
import responses
import uuid
from .cloudrun import Cloudrun
from .run import Run

token = uuid.uuid4().hex
id = uuid.uuid4().hex

def test_cloudrun_init():
    assert type(Cloudrun(token)) is Cloudrun
    assert Cloudrun(token).token == token

@responses.activate
def test_run_create():

    data = json.load(open('cloudrun/test_data/run_create.json'))

    responses.add(responses.POST,'https://api.cloudrun.co/v1/wrf',
                  json=data,status=200)

    run = Run(token)
    run.create('wrf','3.9')
    
    assert run.status == 'created'
    assert run.model == 'wrf'
    assert run.version == '3.9'
    assert run.time_created == datetime.datetime(2017,8,16,12,53,31)
    assert run.input_files == []
    assert run.output_files == []
    
def test_run_init():
    assert type(Run(token)) is Run
    assert Run(token).token == token
#    assert Run(token,id).id == id

#def test_cloudrun_get_run_returns_run():
#    assert type(Cloudrun(token).get_run(id)) is Run
