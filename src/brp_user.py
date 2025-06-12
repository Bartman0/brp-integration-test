import os

from locust import HttpUser


class BrpUser(HttpUser):
    _token = os.environ.get("INT_TEST_TOKEN", "test-token")
    _base_url = os.environ.get("INT_TEST_BASE_URL", "http://localhost:5010")
    path = os.environ.get("INT_TEST_PERSONEN_PATH", "/haalcentraal/api/brp/personen")
    host = _base_url
    url = f"{_base_url}{path}"
    headers = {
        "Authorization": _token,
        "Content-Type": "application/json",
        "X-User": "int-test",
        "X-Correlation-Id": f"int-test-{os.getpid()}",
        "X-Task-Description": "int-test",
    }

    def __do_post(self, data):
        return self.client.post(
            url=f"{self.path}",
            headers=self.headers,
            data=data,
        )
