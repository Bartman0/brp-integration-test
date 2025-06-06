from unittest import TestCase

from locust import HttpUser

from run_base import RunBase


class Verblijfplaatshistorie(RunBase):
    def __init__(self, performance_test: bool, duration: int) -> None:
        super(Verblijfplaatshistorie, self).__init__(
            TestVerblijfplaatshistorie,
            VerblijfplaatshistorieUser,
            performance_test,
            duration,
        )


class TestVerblijfplaatshistorie(TestCase):
    pass


class VerblijfplaatshistorieUser(HttpUser):
    pass
