import requests


gl_url = "https://gitlab.ops.mist.io/api/v3/projects/50/trigger/builds"
TOKEN = '170af2ffaf5fd3edb8dbf1022a4f8c'
data = {"token": TOKEN, "ref": 'fix_google_login'}

request = requests.post(gl_url, data=data)
data = request.json()
