from unittest import TestCase

from locust import task

import requests

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext
from util import number_of_days_back_in_time_as_iso

VOLGINDICATIES_PATH = "/kennisgevingen/v1/volgindicaties"
VOLGINDICATIES_EINDDATUM_TOEKOMST = "2099-12-31"
VOLGINDICATIES_TEST_BSN = "900132747"


class Volgindicaties(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestVolgindicaties
        context.performance_class = VolgindicatiesUser
        super(Volgindicaties, self).__init__(context)


class VolgindicatiesUser(BrpUser):
    def __init__(self, environment):
        super().__init__(environment=environment, path=VOLGINDICATIES_PATH)

    # locust does not like me to put this in the super class BrpUser
    def __do_post(self, data):
        return self.client.post(
            url=self.path,
            headers=self.headers,
            data=data,
        )

    def __do_put(self, data):
        return self.client.put(
            url=self.path,
            headers=self.headers,
            data=data,
        )

    def __do_get(self, params):
        return self.client.get(url=self.path, headers=self.headers, params=params)

    @task
    def test_volgindicaties(self):
        self.__do_get(params=None)


class TestVolgindicaties(TestCase):
    __headers = VolgindicatiesUser.headers
    __url = f"{VolgindicatiesUser._base_url}{VOLGINDICATIES_PATH}"

    def test_volgindicaties(self):
        response = self.__do_get(params=None)
        assert response.status_code == 200

    def test_volgindicaties_put(self):
        response = self.__do_put(
            bsn=VOLGINDICATIES_TEST_BSN,
            data={"einddatum": VOLGINDICATIES_EINDDATUM_TOEKOMST},
        )
        assert response.status_code // 100 == 200 // 100

    def test_volgindicaties_delete(self):
        response = self.__do_put(
            bsn=VOLGINDICATIES_TEST_BSN,
            data={"einddatum": number_of_days_back_in_time_as_iso(1)},
        )
        assert response.status_code // 100 == 200 // 100

    def __do_post(self, data) -> requests.Response:
        return requests.post(
            url=self.__url,
            headers=self.__headers,
            json=data,
        )

    def __do_put(self, bsn, data) -> requests.Response:
        return requests.put(
            url=f"{self.__url}/{bsn}",
            headers=self.__headers,
            json=data,
        )

    def __do_get(self, params) -> requests.Response:
        return requests.get(
            url=self.__url,
            headers=self.__headers,
            params=params,
        )
