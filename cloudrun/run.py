"""
run.py
"""
from .api import Api
from datetime import datetime, timedelta
import numpy as np
import os
import requests
import requests_toolbelt
import sys

API_BASE_URL = 'https://api.cloudrun.co'
API_VERSION = 'v1'
API_URL = API_BASE_URL + '/' + API_VERSION

class Run(object):
    """Class to handle all model run metadata
    and provide access to model output."""
    def __init__(self, url, token, id=None):
        """Run constructor."""
        self.model = None
        self.version = None
        self.id = None
        self.status = None
        self.api = Api(url, token)
        if id:
            self.id = id
            self.get()

    def create(self, model, version):
        """Creates a model run."""
        status, body = self.api.create_run(model, version)
        self._update(body)
        #self._catch_error()

    def delete(self):
        """Deletes run data on server."""
        status, body = self.api.delete_run(self.id)
        self._update(body)
        #self._catch_error()

    def get(self):
        """Refreshes the run data from the server."""
        status, body = self.api.get_run(self.id)
        self._update(body)
        #self._catch_error()

    def read_output(self, field, time1=None, time2=None, 
        lon1=None, lat1=None, lon2=None, lat2=None):
        """Slices the model output field."""
        headers = {'Authorization': 'Bearer ' + self.token}
        url = API_URL + '/wrf/' + self.id + '/fields/' + field
        data = {}
        if time1:
            data['time1'] = time1.strftime('%Y-%m-%d_%H:%M:%S')
        if time2:
            data['time2'] = time2.strftime('%Y-%m-%d_%H:%M:%S')
        if lon1:
            data['lon1'] = lon1
        if lat1:
            data['lat1'] = lat1
        if lon2:
            data['lon2'] = lon2
        if lat2:
            data['lat2'] = lat2
        r = requests.get(url, headers=headers, data=data)
        self._set_rate_limit(r)
        if r.status_code == 200:
            resp = r.json()
            field_atts = resp[field.upper()]
            time = np.array([datetime.strptime(t, '%Y-%m-%d_%H:%M:%S')\
                             for t in resp['times']])
            data = np.array(resp['data'])
            return field_atts, time, data
        else:
            raise ValueError('Server responded with ' + str(r.status_code))

    def start(self, cores=None, compute_option_id=None):
        """Starts the run with a specified number of cores 
        or specific compute_option_id."""
        assert not (cores and compute_option_id),\
            'Ambiguous call; pass either cores or compute_option_id'
        assert cores or compute_option_id,\
            'Insufficient args; either cores or compute_option_id must be provided'

        available_cores = [opt['cores'] for opt in self.compute_options]
        available_ids = [opt['compute_option_id'] for opt in self.compute_options]

        if compute_option_id:
            if not compute_option_id in available_ids:
                raise RuntimeError('Invalid compute_option_id')
        else:
            if not cores in available_cores:
                raise RuntimeError('This number of cores is not available')
            compute_option_id = available_ids[available_cores.index(cores)]

        patch = [{
            "op": "replace",
            "path": "/selected_compute_option",
            "value": {"compute_option_id": compute_option_id}
        }]

        status, body = self.api.patch_run(self.id, patch)
        status, body = self.api.start_run(self.id)
        self._update(body)
        #self._catch_error()

    def stop(self):
        """Stops the run."""
        headers = {'Authorization': 'Bearer ' + self.token}
        url = API_URL + '/wrf/' + self.id + '/stop'
        r = requests.post(url, headers=headers)
        self._set_rate_limit(r)
        self._update(r.json())
        self._catch_error()

    def upload(self, filename=None, url=None, progress=True):
        """Upload a local or remote file."""

        if filename and url:
            raise ValueError('Ambiguous call, both filename and url provided')

        if not filename or url:
            raise ValueError('Missing keyword argument, either filename or url required')

        file_multipart = {'file': (os.path.basename(filename),
            open(filename, 'rb'), 'application/octet-stream')}

        encoder = requests_toolbelt.MultipartEncoder(fields=file_multipart)

        if not progress:
            monitor = requests_toolbelt.MultipartEncoderMonitor(
                encoder, upload_callback_nobar)
        else:
            monitor = requests_toolbelt.MultipartEncoderMonitor(
                encoder, upload_callback)

        headers = {
            'Authorization': 'Bearer ' + self.api.token,
            'Origin': 'cloudrun.co',
            'Content-Type': monitor.content_type
        }

        _url = self.api.url + '/runs/' + self.id + '/input'

        r = requests.post(_url, headers=headers, data=monitor)

        if progress:
            sys.stdout.write('\n')
            sys.stdout.flush()

        if r.status_code == 200:
            self.get()
        else:
            raise ValueError('Server responded with ' + str(r.status_code))

    def _catch_error(self):
        """Catches and raises an error."""
        if self.status == 'error':
            raise RuntimeError(self.error['message'])

    def _set_rate_limit(self, response):
        """Sets the number of requests and time
        to reset from response headers."""
        # TODO: enable requests throttling when we 
        # settle on auth levels.
        #self._requests_limit = int(response.headers['requests_limit'])
        #self._requests_remaining = int(response.headers['requests_remaining'])
        #self._time_to_reset = int(response.headers['time_to_reset'])
        pass

    def _update(self, response):
        """Updates Run attributes from response dict."""
        keys = ['compute_config', 'compute_options', 'disk_usage', 
                'error', 'id', 'input_files', 'model', 'output_files', 
                'percent_complete', 'remaining_time', 'required_input_files', 
                'run_name', 'selected_compute_option', 'status', 'version']
        for key in keys:
            setattr(self, key, response[key])
        self.time_created = datetime.strptime(response['time_created'], 
                                              '%Y-%m-%dT%H:%M:%S.%fZ')
        if response['time_started']:
            self.time_started = datetime.strptime(response['time_started'], 
                                                  '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.time_started = None
        if response['time_stopped']:
            self.time_stopped = datetime.strptime(response['time_stopped'], 
                                                  '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.time_stopped = None

    def __repr__(self):
        """Overloads the default __repr__ method."""
        fields = [self.model, self.version, self.id, self.status]
        if any(fields):
            field_string = ' '.join([field for field in fields if field])
            return '<Run ' + field_string + '>'
        else:
            return self


def upload_callback(encoder):
    """Upload progress bar."""
    bar_length = 50
    fraction = encoder.bytes_read / encoder.len
    bar_full = int(fraction * bar_length) * '#'
    bar_empty = (bar_length - int(fraction * bar_length)) * '-'
    sys.stdout.write('\r Uploading: [' + bar_full + bar_empty + '] ' + '%d' % (fraction * 100) + '%')
    sys.stdout.flush()

def upload_callback_nobar(encoder):
    """Helper function to disable progress bar."""
    pass
