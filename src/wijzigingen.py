from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Wijzigingen(RunBase):
    def __init__(self, performance_test: bool, duration: int) -> None:
        super(Wijzigingen, self).__init__(
            TestWijzigingen, WijzigingenUser, performance_test, duration
        )


class TestWijzigingen(TestCase):
    pass


class WijzigingenUser(HttpUser):
    pass
