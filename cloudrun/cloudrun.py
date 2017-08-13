"""
cloudrun.py
"""
from .run import Run

class Cloudrun(object):
    """Class to handle a Cloudrun API session."""
    def __init__(self,token):
        """Cloudrun constructor."""
        self.token = token

    def get_run(self,id):
        """Returns an instance of model run by id."""
        pass

    def get_all_runs(self):
        """Returns a a list of all model runs that are 
        accessible or owned by user."""
        pass
