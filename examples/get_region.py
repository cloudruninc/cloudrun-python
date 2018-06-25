from cloudrun import Api
import os

token = os.environ['CLOUDRUN_API_TOKEN'] + '|' + os.environ['CLOUDRUN_USER_ID']
url = os.environ.get('CLOUDRUN_API_URL') or 'https://api.cloudrun.co/v1'

api = Api(url, token)

status, body = api.get_region(region_id)

print(body)
