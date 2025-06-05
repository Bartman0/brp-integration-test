import unittest
from run_interface import RunInterface


class Wijzigingen(RunInterface):
    def __init__(self, performance_test: bool) -> None:
        self.performance_test = performance_test
        pass

    def run(self):
        unittest.main()
