from unittest import TestCase

from locust import HttpUser

from run_base import RunBase
from run_context import RunContext


class Volgindicaties(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestVolgindicaties
        context.performance_class = VolgindicatiesUser
        super(Volgindicaties, self).__init__(context)


class TestVolgindicaties(TestCase):
    pass


class VolgindicatiesUser(HttpUser):
    pass
