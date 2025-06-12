from unittest import TestCase

import requests
from locust import task

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext


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
        adresseerbaar_object_identificatie = "0518010000832200"
        peildatum = "2020-09-24"
        self.__do_post(
            data=BEWONING_MET_PEILDATUM.format(
                adresseerbaar_object_identificatie, peildatum
            )
        )


class TestBewoning(TestCase):
    __headers = BewoningUser.headers
    __url = f"{BrpUser._base_url}{BEWONING_PATH}"

    def test_simple(self):
        assert 1 == 1

    def test_bewoning_met_peildatum(self):
        adresseerbaar_object_identificatie = "0518010000832200"
        peildatum = "2020-09-24"
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
