import os

from locust import HttpUser


class BrpUser(HttpUser):
    _token = os.environ.get("INT_TEST_TOKEN", "test-token")
    _base_url = os.environ.get("INT_TEST_BASE_URL", "http://localhost:5010")
    host = _base_url
    _headers = {
        "Authorization": _token,
        "Content-Type": "application/json",
        "X-User": "int-test",
        "X-Correlation-Id": f"int-test-{os.getpid()}",
        "X-Task-Description": "int-test",
    }

    def __init__(self, environment, path):
        self._path = path
        super().__init__(environment=environment)

    def __do_post(self, data):
        return self.client.post(
            url=f"{self._path}",
            headers=BrpUser._headers,
            data=data,
        )

    @property
    def headers(self):
        return BrpUser._headers

    @property
    def path(self):
        return self._path
