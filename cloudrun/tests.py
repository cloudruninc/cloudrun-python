import pytest
from cloudrun import Cloudrun

token = '3dbdc7925f6d426a8bccfd77c62fa940'

def test_cloudrun_init():
    assert Cloudrun(token).token == token
