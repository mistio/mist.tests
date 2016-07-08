import requests

gl_url = "https://gitlab.ops.mist.io/api/v3/projects/2/trigger/builds"
TOKEN = 'a5bd4cd5397d2028bf0a4cde3532e4'
data = {"token": TOKEN, "ref": 'mayday_test'}

request = requests.post(gl_url, data=data)
data = request.json()
