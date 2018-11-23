"""
api.py
"""
import requests


class Api:
    """First layer above HTTP API requests."""
    
    def __init__(self, url, token, debug=False, timer=False):
        """Returns a new Cloudrun session."""
        self.base_url = url.rstrip('/')
        self.token = token
        self.debug = debug
        self.timer = timer

        self.headers = {'Authorization': 'Bearer ' + self.token}

    def create_run(self, model, version):
        """Creates a new run."""
        url = self.base_url + '/runs'
        headers = {'Authorization': 'Bearer ' + self.token}
        data = {'model': model, 'version': version}
        r = requests.post(url, headers=headers, data=data)
        return r.status_code, r.json()

    def delete_run(self, runid):
        """Deletes an existing run."""
        url = self.base_url + '/runs/' + runid
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.delete(url, headers=headers)
        return r.status_code, r.json()

    def get_run(self, runid):
        """Returns an existing run."""
        url = self.base_url + '/runs/' + runid
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=headers)
        return r.status_code, r.json()

    def patch_run(self, runid, json_patch):
        """Applies a JSON patch to a run."""
        url = self.base_url + '/runs/' + runid
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.patch(url, headers=headers, json=json_patch)
        return r.status_code, r.json()

    def start_run(self, runid):
        """Starts a run."""
        url = self.base_url + '/runs/' + runid + '/start'
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.post(url, headers=headers)
        return r.status_code, r.json()

    def upload_file(self, runid, filename):
        """Uploads a file to a run."""
        headers = {'Authorization': 'Bearer ' + self.token,
            'Origin': 'cloudrun.co'}
        url = self.base_url + '/runs/' + runid + '/input'
        files = {'file': open(filename, 'rb')}
        r = requests.post(url, headers=headers, files=files)
        return r.status_code, r.json()

    def get_forecast(self, forecast_id):
        """Returns a forecast object."""
        return self._get('/forecasts/' + forecast_id)

    def get_forecasts_due_to_run(self):
        """Returns all pending forecasts that are due to run."""
        return self._get('/forecasts-due-to-run')

    def patch_forecast(self, forecast_id, json_patch):
        """Updates forecast attributes."""
        return self._patch('/forecasts/' + forecast_id, json_patch)

    def start_forecast_run(self, forecast_id):
        """Starts the forecast that has been created."""
        return self._post('/run-forecast/' + forecast_id)

    def complete_forecast(self, forecast_id):
        """Stops the forecast and marks as complete (admin only)."""
        return self._post('/complete-forecast/' + forecast_id)

    def fail_forecast(self, forecast_id):
        """Stops the forecast and marks with error status (admin only)."""
        return self._post('/fail-forecast/' + forecast_id)

    def stop_forecast(self, forecast_id):
        """Stops the forecast and marks as stopped."""
        return self._post('/stop-forecast/' + forecast_id)

    def get_region(self, region_id):
        """Returns the region object."""
        return self._get('/regions/' + region_id)

    def _get(self, path):
        return self._send_request('get', path)

    def _post(self, path):
        return self._send_request('post', path)

    def _patch(self, path, json):
        return self._send_request('patch', path, json)

    def _send_request(self, verb, path, json=None):
        full_url = self.base_url + '/' + path.lstrip('/')
        request_method = getattr(requests, verb)
        response = request_method(full_url, headers=self.headers, json=json)
        return response.status_code, response.json()
