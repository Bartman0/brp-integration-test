from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Bewoning(RunBase):
    def __init__(self, performance_test: bool, duration: int) -> None:
        super(Bewoning, self).__init__(
            TestBewoning, BewoningUser, performance_test, duration
        )


class TestBewoning(TestCase):
    pass


class BewoningUser(HttpUser):
    pass
