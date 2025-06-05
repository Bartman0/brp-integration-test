import unittest
from unittest import TestCase
from run_interface import RunInterface


class Personen(RunInterface):
    def __init__(self, performance_test: bool) -> None:
        self.performance_test = performance_test
        pass

    def run(self):
        unittest.main()


class TestZoekvraagBsn(TestCase):
    def test_simple(self):
        assert 1 == 1
