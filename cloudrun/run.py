"""
run.py
"""
import datetime
import requests

API_BASE_URL = 'https://api.cloudrun.co'
API_VERSION = 'v1'
API_URL = API_BASE_URL+'/'+API_VERSION

class Run(object):
    """Class to handle all model run metadata 
    and provide access to model output."""
    def __init__(self,token,id=None):
        """Run constructor."""
        self.token = token
        if id:
            self.id = id
            self.get()

    def create(self,model,version):
        """Create a model run."""
        url = API_URL+'/wrf'
        headers = {'Authorization':'Bearer '+self.token}
        data = {'version':version}
        r = requests.post(url,headers=headers,data=data)
        self._update(r.json())

    def delete(self):
        """Deletes run data on server."""
        url = API_URL+'/wrf/'+self.id
        headers = {'Authorization':'Bearer '+self.token}
        r = requests.delete(url,headers=headers)
        self._update(r.json())

    def get(self):
        """Refreshes the run data from the server."""
        headers = {'Authorization':'Bearer '+self.token}
        url = API_URL+'/wrf/'+self.id
        r = requests.get(url,headers=headers)
        if r.status_code == 200:
            self._update(r.json())
        else:
            raise ValueError('Server responded with '+str(r.status_code))

    def upload(self,filename=None,url=None):
        """Upload a local or remote file."""

        if filename and url:
            raise ValueError('Ambiguous call, both filename and url provided')

        if not filename or url:
            raise ValueError('Missing keyword argument, either filename or url required')

        headers = {'Authorization':'Bearer '+self.token}
            

    def setup(self):
        """Set up the run Returns compute options."""
        headers = {'Authorization':'Bearer '+self.token}
        url = API_URL+'/wrf/'+self.id+'/setup'
        r = requests.post(url,headers=headers)

    def start(self):
        """Starts the run."""
        headers = {'Authorization':'Bearer '+self.token}
        url = API_URL+'/wrf/'+self.id+'/start'

    def stop(self):
        """Stops the run."""
        headers = {'Authorization':'Bearer '+self.token}
        url = API_URL+'/wrf/'+self.id+'/stop'
        r = requests.post(url,headers=headers)

    def _update(self,response):
        """Updates Run attributes from response dict."""
        keys = ['status','input_files','output_files']
        for key in keys:
            setattr(self,key,response[key])
        self.time_created = datetime.datetime.strptime(response['time_created'],
            '%Y-%m-%dT%H:%M:%S')
        self.model = response['model']['name']
        self.version = response['model']['version']

    def __repr__(self):
        """Overloads the default __repr__ method."""
        if self.model and self.version:
            return '<Run '+self.model+'-'+self.version+' '+self.id[-6:]+' '+self.status+'>'
        else:
            return '<Run '+self.id[-6:]+' '+self.status+'>'
