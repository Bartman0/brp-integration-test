from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Wijzigingen(RunBase):
    def __init__(
        self, performance_test: bool, duration: int, user_count: int, spawn_rate: int
    ) -> None:
        super(Wijzigingen, self).__init__(
            test_class=TestWijzigingen,
            performance_class=WijzigingenUser,
            performance_test=performance_test,
            duration=duration,
            user_count=user_count,
            spawn_rate=spawn_rate,
        )


class TestWijzigingen(TestCase):
    pass


class WijzigingenUser(HttpUser):
    pass
