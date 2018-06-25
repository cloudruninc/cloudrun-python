"""
api.py
"""
import requests


class Api:
    """First layer above HTTP API requests."""
    
    def __init__(self, url, token, debug=False, timer=False):
        """Returns a new Cloudrun session."""
        self.base_url = self._cleanse_url(url)
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
        return self._get('/runs/forecasts/' + forecast_id)

    def get_forecasts_due_to_run(self):
        return self._get('/runs/forecasts-due-to-run')

    def start_forecast_run(self, forecast_id):
        return self._post('/runs/run-forecast/' + forecast_id)

    def patch_forecast(self, forecast_id, json_patch):
        return self._patch('/runs/forecasts/' + forecast_id, json_patch)

    def _get(self, path):
        return self._send_request('get', path)

    def _post(self, path):
        return self._send_request('post', path)

    def _patch(self, path, json):
        return self._send_request('patch', path, json)

    def _send_request(self, verb, path, json=None):
        full_url = self.base_url + '/' + self._cleanse_path(path)
        request_method = getattr(requests, verb)
        response = request_method(full_url, headers=self.headers, json=json)
        return response.status_code, response.json()

    def _cleanse_url(self, url):
        # strip trailing slash from url
        if url.endswith('/'):
            return url[:-1]
        else:
            return url

    def _cleanse_path(self, path):
        # strip leading slash from path
        if path.startswith('/'):
            return path[1:]
        else:
            return path
