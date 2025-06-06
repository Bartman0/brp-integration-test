from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Volgindicaties(RunBase):
    def __init__(self, performance_test: bool, duration: int) -> None:
        super(Volgindicaties, self).__init__(
            TestVolgindicaties, VolgindicatiesUser, performance_test, duration
        )


class TestVolgindicaties(TestCase):
    pass


class VolgindicatiesUser(HttpUser):
    pass
