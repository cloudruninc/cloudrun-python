from cloudrun import Api
import os
import json

token = os.environ['CLOUDRUN_API_TOKEN']
url = os.environ.get('CLOUDRUN_API_URL') or 'https://api.cloudrun.co/v1'

api = Api(url, token)

status, forecasts = api.get_forecasts_due_to_run()

for forecast in forecasts:
    print(json.dumps(forecast))
