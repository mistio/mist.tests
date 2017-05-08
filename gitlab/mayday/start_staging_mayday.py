import requests


gl_url = "https://gitlab.ops.mist.io/api/v3/projects/50/trigger/builds"
TOKEN = ''
data = {"token": TOKEN, "ref": 'staging_mayday'}

request = requests.post(gl_url, data=data)
data = request.json()
