import datetime
import json
import responses
import uuid
from .run import Run

url = 'https://api.cloudrun.co/v1'
token = uuid.uuid4().hex

def test_run_init():
    assert type(Run(url, token)) is Run
    assert Run(url, token).api.token == token


@responses.activate
def test_run_create():

    data = json.load(open('cloudrun/test_data/run_create.json'))
    headers = {
        'requests_limit': '1000',
        'requests_remaining': '778',
        'time_to_reset': '1234',
    }

    responses.add(responses.POST, url + '/runs', json=data,
                  status=200, headers=headers)

    run = Run(url, token)
    run.create('wrf', '3.9.1')
    
    assert run.compute_config == {}
    assert run.compute_options == []
    assert run.disk_usage == 0
    assert run.error == None
    assert run.id == "5c6b0737-af4e-4168-b9b7-46e5f25e0e1a"
    assert run.input_files == []
    assert run.model == 'wrf'
    assert run.output_files == []
    assert run.required_input_files == ['namelist.input']
    assert run.run_name == None
    assert run.selected_compute_option == {}
    assert run.status == 'created'
    assert run.time_created == datetime.datetime(2018, 5, 30, 16, 55, 3, 605352)
    assert run.time_started == None
    assert run.time_stopped == None
    assert run.version == '3.9.1'
