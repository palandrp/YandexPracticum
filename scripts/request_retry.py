import requests

from requests.adapters import HTTPAdapter, Retry


DEFAULT_TIMEOUT = 5  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


retries = Retry(total=8, backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)

http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
