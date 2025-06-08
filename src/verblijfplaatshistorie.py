from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Verblijfplaatshistorie(RunBase):
    def __init__(
        self, performance_test: bool, duration: int, user_count: int, spawn_rate: int
    ) -> None:
        super(Verblijfplaatshistorie, self).__init__(
            test_class=TestVerblijfplaatshistorie,
            performance_class=VerblijfplaatshistorieUser,
            performance_test=performance_test,
            duration=duration,
            user_count=user_count,
            spawn_rate=spawn_rate,
        )


class TestVerblijfplaatshistorie(TestCase):
    pass


class VerblijfplaatshistorieUser(HttpUser):
    pass
