from dataclasses import dataclass
from unittest import TestCase

from locust import User


@dataclass
class RunContext:
    test_class: type[TestCase]
    performance_class: type[User]
    performance_test: bool
    duration: int
    user_count: int
    spawn_rate: int
    avg_response_time_limit: int
