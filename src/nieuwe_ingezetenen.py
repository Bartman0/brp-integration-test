from unittest import TestCase

import requests
from locust import task

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext

from datetime import datetime, timedelta


NIEUWE_INGEZETENEN_PATH = "/haalcentraal/api/nieuwe-ingezetenen"


class NieuweIngezetenen(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestNieuweIngezetenen
        context.performance_class = NieuweIngezetenenUser
        super(NieuweIngezetenen, self).__init__(context)


def number_of_days_back_in_time_as_iso(days: int):
    return (datetime.today() - timedelta(days)).strftime("%Y-%m-%d")


class NieuweIngezetenenUser(BrpUser):
    def __init__(self, environment):
        super().__init__(environment=environment, path=NIEUWE_INGEZETENEN_PATH)

    # locust does not like me to put this in the super class BrpUser
    def __do_get(self, params):
        return self.client.get(url=self.path, headers=self.headers, params=params)

    @task
    def test_nieuwe_ingezetenen(self):
        self.__do_get(params={"vanaf": number_of_days_back_in_time_as_iso(14)})


class TestNieuweIngezetenen(TestCase):
    __headers = NieuweIngezetenenUser.headers
    __url = f"{BrpUser._base_url}{NIEUWE_INGEZETENEN_PATH}"

    def test_simple(self):
        assert 1 == 1

    def test_nieuwe_ingezetenen(self):
        response = self.__do_get(
            params={"vanaf": number_of_days_back_in_time_as_iso(14)}
        )
        assert response.status_code == 200

    def __do_get(self, params) -> requests.Response:
        return requests.get(url=f"{self.__url}", headers=self.__headers, params=params)
