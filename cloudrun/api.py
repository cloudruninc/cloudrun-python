"""
api.py
"""
import requests

class Api():
    """First layer above HTTP API requests."""
    
    def __init__(self, url, token, debug=False, timer=False):
        """Returns a new Cloudrun session."""
        self.url = url
        self.token = token
        self.debug = debug
        self.timer = timer

    def create_run(self, model, version):
        """Creates a new run."""
        url = self.url + '/runs'
        headers = {'Authorization': 'Bearer ' + self.token}
        data = {'model': model, 'version': version}
        r = requests.post(url, headers=headers, data=data)
        return r.status_code, r.json()

    def delete_run(self, runid):
        """Deletes an existing run."""
        url = self.url + '/runs/' + runid
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.delete(url, headers=headers)
        return r.status_code, r.json()

    def get_run(self, runid):
        """Returns an existing run."""
        url = self.url + '/runs/' + runid
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=headers)
        return r.status_code, r.json()

    def patch_run(self, runid, json_patch):
        """Applies a JSON patch to a run."""
        url = self.url + '/runs/' + runid
        headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=headers, json=json_patch)
        return r.status_code, r.json()

    def upload_file(self, runid, filename):
        """Uploads a file to a run."""
        headers = {'Authorization': 'Bearer ' + self.token,
            'Origin': 'cloudrun.co'}
        url = self.url + '/runs/' + runid + '/input'
        files = {'file': open(filename, 'rb')}
        r = requests.post(url, headers=headers, files=files)
        return r.status_code, r.json()
