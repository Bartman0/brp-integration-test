from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Volgindicaties(RunBase):
    def __init__(
        self, performance_test: bool, duration: int, user_count: int, spawn_rate: int
    ) -> None:
        super(Volgindicaties, self).__init__(
            test_class=TestVolgindicaties,
            performance_class=VolgindicatiesUser,
            performance_test=performance_test,
            duration=duration,
            user_count=user_count,
            spawn_rate=spawn_rate,
        )


class TestVolgindicaties(TestCase):
    pass


class VolgindicatiesUser(HttpUser):
    pass
