"""
run.py
"""
import requests

API_BASE_URL = 'https://api.cloudrun.co'
API_VERSION = 'v1'
API_URL = API_BASE_URL+'/'+API_VERSION

class Run(object):
    """Class to handle all model run metadata 
    and provide access to model output."""
    def __init__(self,token,id):
        """Run constructor."""
        self.token = token
        self.id = id

    def create(self,model,version):
        """Create a model run."""
        pass

    def delete(self):
        """Deletes run data on server."""
        pass

    def get(self):
        """Refreshes the run data from the server."""
        pass

    def upload(self,filename=None,url=None):
        """Upload a local or remote file."""
        pass

    def start(self):
        """Starts the run."""
        pass

    def stop(self):
        """Stops the run."""
        pass
