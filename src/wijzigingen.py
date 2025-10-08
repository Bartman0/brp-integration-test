from unittest import TestCase

import requests

from locust import task

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext
from util import number_of_days_back_in_time_as_iso

WIJZIGINGEN_PATH = "/kennisgevingen/v1/wijzigingen"


# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
#
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1


class Wijzigingen(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestWijzigingen
        context.performance_class = WijzigingenUser
        super(Wijzigingen, self).__init__(context)


class WijzigingenUser(BrpUser):
    def __init__(self, environment):
        super().__init__(environment=environment, path=WIJZIGINGEN_PATH)

    # locust does not like me to put this in the super class BrpUser
    def __do_post(self, data):
        return self.client.post(
            url=self.path,
            headers=self.headers,
            data=data,
        )

    def __do_get(self, params):
        return self.client.get(url=self.path, headers=self.headers, params=params)

    @task
    def test_wijzigingen(self):
        self.__do_get(params={"vanaf": number_of_days_back_in_time_as_iso(31)})


class TestWijzigingen(TestCase):
    __headers = WijzigingenUser.headers
    __url = f"{WijzigingenUser._base_url}{WIJZIGINGEN_PATH}"

    def test_wijzigingen(self):
        response = self.__do_get(
            params={"vanaf": number_of_days_back_in_time_as_iso(31)}
        )
        assert response.status_code == 200

    def __do_post(self, data) -> requests.Response:
        return requests.post(
            url=self.__url,
            headers=self.__headers,
            data=data,
        )

    def __do_get(self, params) -> requests.Response:
        return requests.get(
            url=self.__url,
            headers=self.__headers,
            params=params,
        )
