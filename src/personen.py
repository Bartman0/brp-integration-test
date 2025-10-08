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
PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER = (
    '{{"type": "ZoekMetPostcodeEnHuisnummer", "postcode": "{}", "huisnummer": "{}"}}'
)

PERSONEN_PATH = "/bevragingen/v1/personen"

PERSONEN_TEST_BSN = "999972030"
PERSONEN_TEST_POSTCODE = "1014CB"
PERSONEN_TEST_HUISNUMMER = "20"

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
        burgerservicenummer = PERSONEN_TEST_BSN
        self.__do_post(data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer))

    @task
    def test_zoekvraag_postcode_huisnummer(self):
        postcode = PERSONEN_TEST_POSTCODE
        huisnummer = PERSONEN_TEST_HUISNUMMER
        self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )

    @task
    def test_zoekvraag_postcode_huisnummer_en_bsn(self):
        postcode = PERSONEN_TEST_POSTCODE
        huisnummer = PERSONEN_TEST_HUISNUMMER
        self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )


class TestPersonen(TestCase):
    __headers = PersonenUser.headers
    __url = f"{BrpUser._base_url}{PERSONEN_PATH}"

    def test_zoekvraag_bsn(self):
        burgerservicenummer = PERSONEN_TEST_BSN
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer)
        )
        assert response.status_code == 200

    def test_zoekvraag_postcode_huisnummer(self):
        postcode = PERSONEN_TEST_POSTCODE
        huisnummer = PERSONEN_TEST_HUISNUMMER
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )
        assert response.status_code == 200

    def test_zoekvraag_postcode_huisnummer_en_bsn(self):
        postcode = PERSONEN_TEST_POSTCODE
        huisnummer = PERSONEN_TEST_HUISNUMMER
        response = self.__do_post(
            data=PERSONEN_ZOEKVRAAG_POSTCODE_HUISNUMMER.format(postcode, huisnummer)
        )
        assert response.status_code == 200
        # use the first burgerservicenummer returned as input for a bsn zoekvraag query
        burgerservicenummer = response.json()["personen"][0]["burgerservicenummer"]
        self.__do_post(data=PERSONEN_ZOEKVRAAG_BSN.format(burgerservicenummer))
        assert response.status_code == 200

    def __do_post(self, data) -> requests.Response:
        return requests.post(
            url=self.__url,
            headers=self.__headers,
            data=data,
        )
