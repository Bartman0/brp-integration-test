import os
from unittest import TestCase

import requests
from locust import HttpUser, task
import locust.stats

from run_base import RunBase

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 1

# format strings, so accolades need to be repeated to be part of the result as in JSON constructs
PERSONEN_ZOEKVRAAG_BSN = '{{"type": "RaadpleegMetBurgerservicenummer", "burgerservicenummer": [{}], "fields": ["burgerservicenummer"]}}'
PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER = '{{"type": "ZoekMetPostcodeEnHuisnummer", "postcode": "{}", "huisnummer": "{}", "fields": ["burgerservicenummer", "naam"]}}'


class Personen(RunBase):
    def __init__(
        self, performance_test: bool, duration: int, user_count: int, spawn_rate: int
    ) -> None:
        super(Personen, self).__init__(
            test_class=TestPersonen,
            performance_class=PersonenUser,
            performance_test=performance_test,
            duration=duration,
            user_count=user_count,
            spawn_rate=spawn_rate,
        )


class PersonenUser(HttpUser):
    _token = os.environ.get("INT_TEST_TOKEN", "test-token")
    headers = {
        "Authorization": _token,
        "Content-Type": "application/json",
        "X-User": "int-test",
        "X-Correlation-Id": f"int-test-{os.getpid()}",
        "X-Task-Description": "int-test",
    }
    _base_url = os.environ.get("INT_TEST_BASE_URL", "http://localhost:5010")
    host = _base_url
    path = os.environ.get("INT_TEST_PERSONEN_PATH", "/haalcentraal/api/brp/personen")
    url = f"{_base_url}{path}"

    @task
    def test_zoekvraag_bsn(self):
        burgerservicenummer = 999993653
        self.__do_post(data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer))

    @task
    def test_zoekvraag_postcode_huisnummer(self):
        postcode = "3078CE"
        huisnummer = "1"
        self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )

    @task
    def test_zoekvraag_postcode_huisnummer_en_bsn(self):
        postcode = "3078CE"
        huisnummer = "1"
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )
        burgerservicenummer = response.json()["personen"][0]["burgerservicenummer"]
        self.__do_post(data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer))

    def __do_post(self, data):
        return self.client.post(
            url=f"{self.path}",
            headers=self.headers,
            data=data,
        )


class TestPersonen(TestCase):
    _headers = PersonenUser.headers
    _url = PersonenUser.url

    def test_simple(self):
        assert 1 == 1

    def test_zoekvraag_bsn(self):
        burgerservicenummer = 999993653
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer)
        )
        assert response.status_code == 200

    def test_zoekvraag_postcode_huisnummer(self):
        postcode = "3078CE"
        huisnummer = "1"
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )
        assert response.status_code == 200

    @task
    def test_zoekvraag_postcode_huisnummer_en_bsn(self):
        postcode = "3078CE"
        huisnummer = "1"
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )
        assert response.status_code == 200
        burgerservicenummer = response.json()["personen"][0]["burgerservicenummer"]
        self.__do_post(data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer))
        assert response.status_code == 200

    def __do_post(self, data) -> requests.Response:
        return requests.post(
            url=f"{self._url}",
            headers=self._headers,
            data=data,
        )
