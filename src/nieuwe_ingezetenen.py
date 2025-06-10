from unittest import TestCase

from locust import HttpUser

from run_base import RunBase
from run_context import RunContext


class NieuweIngezetenen(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestNieuweIngezetenen
        context.performance_class = NieuweIngezetenenUser
        super(NieuweIngezetenen, self).__init__(context)


class TestNieuweIngezetenen(TestCase):
    pass


class NieuweIngezetenenUser(HttpUser):
    pass
