from unittest import TestCase

import requests
from locust import task

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext
from util import number_of_days_back_in_time_as_iso

BEWONING_MET_PEILDATUM = '{{"type": "BewoningMetPeildatum", "adresseerbaarObjectIdentificatie": "{}", "peildatum": "{}"}}'
BEWONING_TEST_ID = "0363010000909061"
BEWONING_TEST_PEILDATUM = number_of_days_back_in_time_as_iso(14)


BEWONING_PATH = "/bevragingen/v1/bewoningen"


# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
#
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1


BEWONING_MET_PEILDATUM = '{{"type": "BewoningMetPeildatum", "adresseerbaarObjectIdentificatie": "{}", "peildatum": "{}"}}'

BEWONING_PATH = "/haalcentraal/api/bewoning/bewoningen"


class Bewoning(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestBewoning
        context.performance_class = BewoningUser
        super(Bewoning, self).__init__(context)


class BewoningUser(BrpUser):
    def __init__(self, environment):
        super().__init__(environment=environment, path=BEWONING_PATH)

    # locust does not like me to put this in the super class BrpUser
    def __do_post(self, data):
        return self.client.post(
            url=self.path,
            headers=self.headers,
            data=data,
        )

    @task
    def test_bewoning_met_peildatum(self):
        adresseerbaar_object_identificatie = BEWONING_TEST_ID
        peildatum = BEWONING_TEST_PEILDATUM
        self.__do_post(
            data=BEWONING_MET_PEILDATUM.format(
                adresseerbaar_object_identificatie, peildatum
            )
        )


class TestBewoning(TestCase):
    __headers = BewoningUser.headers
    __url = f"{BrpUser._base_url}{BEWONING_PATH}"

    def test_bewoning_met_peildatum(self):
        adresseerbaar_object_identificatie = BEWONING_TEST_ID
        peildatum = BEWONING_TEST_PEILDATUM
        response = self.__do_post(
            data=BEWONING_MET_PEILDATUM.format(
                adresseerbaar_object_identificatie, peildatum
            )
        )
        assert response.status_code == 200

    def __do_post(self, data) -> requests.Response:
        return requests.post(
            url=f"{self.__url}",
            headers=self.__headers,
            data=data,
        )
