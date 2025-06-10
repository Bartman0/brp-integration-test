from unittest import TestCase

from locust import HttpUser

from run_base import RunBase
from run_context import RunContext


class Verblijfplaatshistorie(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestVerblijfplaatshistorie
        context.performance_class = VerblijfplaatshistorieUser
        super(Verblijfplaatshistorie, self).__init__(context)


class TestVerblijfplaatshistorie(TestCase):
    pass


class VerblijfplaatshistorieUser(HttpUser):
    pass
