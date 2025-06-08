from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class NieuweIngezetenen(RunBase):
    def __init__(
        self, performance_test: bool, duration: int, user_count: int, spawn_rate: int
    ) -> None:
        super(NieuweIngezetenen, self).__init__(
            test_class=TestNieuweIngezetenen,
            performance_class=NieuweIngezetenenUser,
            performance_test=performance_test,
            duration=duration,
            user_count=user_count,
            spawn_rate=spawn_rate,
        )


class TestNieuweIngezetenen(TestCase):
    pass


class NieuweIngezetenenUser(HttpUser):
    pass
