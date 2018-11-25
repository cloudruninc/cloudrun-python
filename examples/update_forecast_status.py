from cloudrun import Api
import os
import json

token = os.environ['CLOUDRUN_API_TOKEN']
url = os.environ.get('CLOUDRUN_API_URL') or 'https://api.cloudrun.co/v1'

api = Api(url, token)

patch = [
    {"op": "replace", "path": "/status", "value": 'pending'},
    {"op": "replace", "path": "/status_percent_complete", "value": 44}]

status, forecast = api.patch_forecast('dfbb92d1-5e46-4505-8f6f-f8af1ac07012', patch)

print(json.dumps(forecast))
