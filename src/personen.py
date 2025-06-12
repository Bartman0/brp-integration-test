import os
from unittest import TestCase

import locust.stats
import requests
from locust import task

from run_base import RunBase
from run_context import RunContext
from brp_user import BrpUser
from token_util import Token

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 1

# format strings, so accolades need to be repeated to be part of the result as in JSON constructs
PERSONEN_ZOEKVRAAG_BSN = '{{"type": "RaadpleegMetBurgerservicenummer", "burgerservicenummer": [{}], "fields": ["burgerservicenummer"]}}'
PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER = '{{"type": "ZoekMetPostcodeEnHuisnummer", "postcode": "{}", "huisnummer": "{}", "fields": ["burgerservicenummer", "naam"]}}'

PERSONEN_PATH = "/haalcentraal/api/brp/personen"

TOKEN = Token(os.environ.get("INT_TEST_TOKEN", "int-test-token"))
ROLES = TOKEN.roles


class Personen(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestPersonen
        context.performance_class = PersonenUser
        super().__init__(context)


class PersonenUser(BrpUser):
    def __init__(self, environment):
        super().__init__(environment=environment, path=PERSONEN_PATH)

    # locust does not like me to put this in the super class BrpUser
    def __do_post(self, data):
        return self.client.post(
            url=self.path,
            headers=self.headers,
            data=data,
        )

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
        # use the first burgerservicenummer returned as input for a bsn zoekvraag query
        burgerservicenummer = response.json()["personen"][0]["burgerservicenummer"]
        self.__do_post(data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer))


class TestPersonen(TestCase):
    __headers = PersonenUser.headers
    __url = f"{BrpUser._base_url}{PERSONEN_PATH}"

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
            url=f"{self.__url}",
            headers=self.__headers,
            data=data,
        )
