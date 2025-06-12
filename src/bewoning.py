from unittest import TestCase

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext


class Bewoning(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestBewoning
        context.performance_class = BewoningUser
        super(Bewoning, self).__init__(context)


class TestBewoning(TestCase):
    pass


class BewoningUser(BrpUser):
    pass
