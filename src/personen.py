import os
import unittest
from unittest import TestCase

import requests
from locust import HttpUser, task
from locust.env import Environment
from locust.stats import stats_printer
import gevent

from run_interface import RunInterface


class Personen(RunInterface):
    def __init__(self, performance_test: bool) -> None:
        self.performance_test = performance_test

    def run(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPersonen)
        unittest.TextTestRunner(verbosity=2).run(suite)
        if self.performance_test:
            env = Environment(user_classes=[PersonenUser])
            runner = env.create_local_runner()
            runner.start(user_count=10, spawn_rate=20)
            gevent.spawn(stats_printer(env.stats))
            gevent.spawn_later(3, runner.quit)
            runner.greenlet.join()


class PersonenUser(HttpUser):
    headers = {"Content-Type": "application/json"}
    _base_url = os.environ.get("INT_TEST_PERSONEN_BASE_URL", "http://localhost:5010")
    host = _base_url
    path = os.environ.get("INT_TEST_PERSONEN_PATH", "/haalcentraal/api/brp/personen")
    url = f"{_base_url}{path}"

    @task
    def test_zoekvraag_bsn(self):
        self.client.post(
            url=f"{self.path}",
            headers=self.headers,
            data='{"type": "RaadpleegMetBurgerservicenummer", "burgerservicenummer": ["999993653"], "fields": ["burgerservicenummer"]}',
        )


class TestPersonen(TestCase):
    _headers = PersonenUser.headers
    _url = PersonenUser.url

    def test_simple(self):
        assert 1 == 1

    def test_zoekvraag_bsn(self):
        response = requests.post(
            url=f"{self._url}",
            headers=self._headers,
            data='{"type": "RaadpleegMetBurgerservicenummer", "burgerservicenummer": ["999993653"], "fields": ["burgerservicenummer"]}',
        )
        assert response.status_code == 200

    def test_zoekvraag_postcode_huisnummer(self):
        response = requests.post(
            url=f"{self._url}",
            headers=self._headers,
            data='{"type": "ZoekMetPostcodeEnHuisnummer", "postcode": "3078CE", "huisnummer": "1", "fields": ["naam"]}',
        )
        assert response.status_code == 200
