from unittest import TestCase

from brp_user import BrpUser
from run_base import RunBase
from run_context import RunContext


class NieuweIngezetenen(RunBase):
    def __init__(self, context: RunContext) -> None:
        context.test_class = TestNieuweIngezetenen
        context.performance_class = NieuweIngezetenenUser
        super(NieuweIngezetenen, self).__init__(context)


class TestNieuweIngezetenen(TestCase):
    pass


class NieuweIngezetenenUser(BrpUser):
    pass
