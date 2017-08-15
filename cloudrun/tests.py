import pytest
import uuid
from .cloudrun import Cloudrun
from .run import Run

token = uuid.uuid4().hex
id = uuid.uuid4().hex

def test_cloudrun_init():
    assert type(Cloudrun(token)) is Cloudrun
    assert Cloudrun(token).token == token

#def test_run_init():
#    assert type(Run(token,id)) is Run
#    assert Run(token,id).token == token
#    assert Run(token,id).id == id

#def test_cloudrun_get_run_returns_run():
#    assert type(Cloudrun(token).get_run(id)) is Run
