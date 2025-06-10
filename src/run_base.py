import unittest
from dumper import dump
from unittest import TestCase

import gevent
from locust import User
from locust.env import Environment
from locust.stats import RequestStats, stats_printer


class RunBase:
    def __init__(
        self,
        test_class: type[TestCase],
        performance_class: type[User],
        performance_test: bool,
        duration: int,
        user_count: int,
        spawn_rate: int,
        avg_response_time_limit: int,
    ):
        self._performance_test: bool = performance_test
        self._test_class: type[TestCase] = test_class
        self._performance_class: type[User] = performance_class
        self._duration: int = duration
        self._user_count: int = user_count
        self._spawn_rate: int = spawn_rate
        self._avg_response_time_limit = avg_response_time_limit

    def run(self):
        # perform the functional tests
        suite = unittest.TestLoader().loadTestsFromTestCase(self._test_class)
        unittest.TextTestRunner(verbosity=2).run(suite)
        if self._performance_test:
            # perform the performance tests
            env = Environment(user_classes=[self._performance_class])
            runner = env.create_local_runner()
            runner.start(user_count=self._user_count, spawn_rate=self._spawn_rate)
            gevent.spawn(stats_printer(env.stats))
            gevent.spawn_later(self._duration, runner.quit)
            runner.greenlet.join()
            self.check_results(env.stats)

    def check_results(self, stats: RequestStats):
        # this dump() is just for debugging/logging, will be removed soon
        dump(stats)
        if stats.num_failures > 0:
            raise RuntimeError("error executing performance tests")
        # all requests are considered equal here, average response time should be below this limit
        if (
            stats.total.total_response_time / stats.num_requests
        ) > self._avg_response_time_limit:
            raise RuntimeError("average response time limit exceeded")
        # TODO enhance with performance checks
