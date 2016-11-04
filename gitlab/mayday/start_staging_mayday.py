import requests

gl_url = "https://gitlab.ops.mist.io/api/v3/projects/29/trigger/builds"
TOKEN = 'ededbd99791f66c6a958b70c8689d7'
data = {"token": TOKEN, "ref": 'staging_mayday'}

request = requests.post(gl_url, data=data)
data = request.json()
