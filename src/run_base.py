import unittest

import gevent
from locust.env import Environment
from locust.stats import RequestStats, stats_printer

from run_context import RunContext


class RunBase:
    def __init__(self, context: RunContext):
        self.context = context

    def run(self):
        # perform the functional tests
        suite = unittest.TestLoader().loadTestsFromTestCase(self.context.test_class)
        unittest.TextTestRunner(verbosity=2).run(suite)
        if self.context.performance_test:
            # perform the performance tests
            env = Environment(user_classes=[self.context.performance_class])
            runner = env.create_local_runner()
            runner.start(
                user_count=self.context.user_count, spawn_rate=self.context.spawn_rate
            )
            gevent.spawn(stats_printer(env.stats))
            gevent.spawn_later(self.context.duration, runner.quit)
            runner.greenlet.join()
            self.check_results(env.stats)

    def check_results(self, stats: RequestStats):
        # this dump() is just for debugging/logging, will be removed soon
        # dump(stats)
        if stats.num_failures > 0:
            raise RuntimeError("error executing performance tests")
        # all requests are considered equal here, average response time should be below this limit
        average_response_time = stats.total.total_response_time / stats.num_requests
        print(f"average response time (ms): {average_response_time}")
        if average_response_time > self.context.avg_response_time_limit:
            raise RuntimeError("average response time limit exceeded")
        # TODO enhance with performance checks
