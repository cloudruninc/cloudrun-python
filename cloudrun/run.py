"""
run.py
"""
import datetime
import requests
import requests_toolbelt
import sys

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
        """Creates a model run."""
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

    def setup(self):
        """Set up the run Returns compute options."""
        headers = {'Authorization':'Bearer '+self.token}
        url = API_URL+'/wrf/'+self.id+'/setup'
        r = requests.post(url,headers=headers)
        if r.status_code == 200:
            resp = r.json()
            self.compute_options = resp['compute_options']
            self.required_input_files = resp['required_input_files']
        else:
            raise ValueError('Server responded with '+str(r.status_code))

    def start(self,cores):
        """Starts the run with a specified number of cores."""
        headers = {'Authorization':'Bearer '+self.token}
        data = {'cores':cores}
        url = API_URL+'/wrf/'+self.id+'/start'
        r = requests.post(url,headers=headers,data=data)
        self._update(r.json())

    def stop(self):
        """Stops the run."""
        headers = {'Authorization':'Bearer '+self.token}
        url = API_URL+'/wrf/'+self.id+'/stop'
        r = requests.post(url,headers=headers)
        self._update(r.json())


    def upload(self,filename=None,url=None,progress=True):
        """Upload a local or remote file."""

        if filename and url:
            raise ValueError('Ambiguous call, both filename and url provided')

        if not filename or url:
            raise ValueError('Missing keyword argument, either filename or url required')

        if filename:
            _url = API_URL+'/wrf/'+self.id+'/upload'
        elif url:
            _url = API_URL+'/wrf/'+self.id+'/upload_url'
 
        encoder = requests_toolbelt.MultipartEncoder(\
            fields={'file':(filename,open(filename,'rb'),'application/octet-stream')})

        if not progress:
            monitor = requests_toolbelt.MultipartEncoderMonitor(encoder,upload_callback_nobar)
        else:
            monitor = requests_toolbelt.MultipartEncoderMonitor(encoder,upload_callback)

        headers = {'Authorization':'Bearer '+self.token,\
                   'Origin':'cloudrun.co',\
                   'Content-Type': monitor.content_type}

        r = requests.post(_url,headers=headers,data=monitor)

        if r.status_code == 200:
            self.get()
        else:
            raise ValueError('Server responded with '+str(r.status_code))

    def _update(self,response):
        """Updates Run attributes from response dict."""
        keys = ['error','id','status','input_files','required_input_files',
            'output_files','percent_complete','remaining_time']
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
    

def upload_callback(encoder):
    """Upload progress bar."""
    bar_length = 50
    fraction = encoder.bytes_read / encoder.len
    bar_full = int(fraction * bar_length) * '#'
    bar_empty = (bar_length - int(fraction * bar_length)) * '-'
    sys.stdout.write('\r Uploading: ['+bar_full+bar_empty+'] '+'%d' % (fraction * 100) + '%')
    sys.stdout.flush()

def upload_callback_nobar(encoder):
    pass
