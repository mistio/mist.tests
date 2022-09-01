import requests


class MistRequests(object):
    """
    Simple class to make requests with or without cookies etc.
    This way we can have the same request methods both in CE and EE/HS
    """

    def __init__(self, uri, params=None, data=None, json=None, cookie=None,
                 timeout=None, csrf_token=None, api_token=None,
                 allow_redirects=False):
        self.headers = {}
        if cookie:
            self.headers.update({'Cookie': cookie})
        if csrf_token:
            self.headers.update({'Csrf-Token': csrf_token})
        if api_token:
            self.headers.update({'Authorization': api_token})
        self.timeout = timeout
        self.uri = uri
        self.data = data
        self.params = params
        self.json = json
        self.allow_redirects = allow_redirects

    def post(self):
        response = requests.post(self.uri, params=self.params, data=self.data,
                                 json=self.json, headers=self.headers,
                                 timeout=self.timeout,
                                 allow_redirects=self.allow_redirects)
        return response

    def get(self):
        response = requests.get(self.uri, params=self.params,
                                headers=self.headers, timeout=self.timeout)
        return response

    def put(self):
        response = requests.put(self.uri, params=self.params, data=self.data,
                                json=self.json, headers=self.headers,
                                timeout=self.timeout)
        return response

    def patch(self):
        response = requests.patch(self.uri, params=self.params, data=self.data,
                                  json=self.json, headers=self.headers,
                                  timeout=self.timeout)
        return response

    def delete(self):
        response = requests.delete(self.uri, params=self.params,
                                   data=self.data, json=self.json,
                                   headers=self.headers,
                                   timeout=self.timeout)
        return response

    def unavailable_api_call(self, *args, **kwargs):
        raise NotImplementedError("This method call is not available")
