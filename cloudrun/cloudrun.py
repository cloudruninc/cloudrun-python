"""
cloudrun.py
"""
from .run import Run

class Cloudrun(object):
    """Class to handle a Cloudrun API session."""
    def __init__(self, token):
        """Cloudrun constructor."""
        self.token = token

    def create_run(self, model, version):
        """Creates a new Run instance."""
        run = Run(self.token)
        run.create(model, version)
        return run

    def get_run(self, id):
        """Returns an instance of model run by id."""
        return Run(self.token, id)

    def get_all_runs(self):
        """Returns a a list of all model runs that are 
        accessible or owned by user."""
        # TODO get list of all IDs that belong to user
        # TODO fetch each run by ID.
        pass
