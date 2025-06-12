from unittest import TestCase

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext


class Wijzigingen(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestWijzigingen
        context.performance_class = WijzigingenUser
        super(Wijzigingen, self).__init__(context)


class TestWijzigingen(TestCase):
    pass


class WijzigingenUser(BrpUser):
    pass
