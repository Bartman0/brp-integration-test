import unittest
from unittest import TestCase

import gevent
from locust import User
from locust.env import Environment
from locust.stats import stats_printer


class RunBase:
    def __init__(
        self,
        test_class: type[TestCase],
        performance_class: type[User],
        performance_test: bool,
        duration: int,
        user_count: int,
        spawn_rate: int,
    ):
        self._performance_test: bool = performance_test
        self._test_class: type[TestCase] = test_class
        self._performance_class: type[User] = performance_class
        self._duration: int = duration
        self._user_count: int = user_count
        self._spawn_rate: int = spawn_rate

    def run(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(self._test_class)
        unittest.TextTestRunner(verbosity=2).run(suite)
        if self._performance_test:
            env = Environment(user_classes=[self._performance_class])
            runner = env.create_local_runner()
            runner.start(user_count=self._user_count, spawn_rate=self._spawn_rate)
            gevent.spawn(stats_printer(env.stats))
            gevent.spawn_later(self._duration, runner.quit)
            runner.greenlet.join()
