from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class NieuweIngezetenen(RunBase):
    def __init__(self, performance_test: bool, duration: int) -> None:
        super(NieuweIngezetenenUser, self).__init__(
            TestNieuweIngezetenen, NieuweIngezetenenUser, performance_test, duration
        )


class TestNieuweIngezetenen(TestCase):
    pass


class NieuweIngezetenenUser(HttpUser):
    pass
