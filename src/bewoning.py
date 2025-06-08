from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Bewoning(RunBase):
    def __init__(
        self, performance_test: bool, duration: int, user_count: int, spawn_rate: int
    ) -> None:
        super(Bewoning, self).__init__(
            test_class=TestBewoning,
            performance_class=BewoningUser,
            performance_test=performance_test,
            duration=duration,
            user_count=user_count,
            spawn_rate=spawn_rate,
        )


class TestBewoning(TestCase):
    pass


class BewoningUser(HttpUser):
    pass
