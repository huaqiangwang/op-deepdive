import unittest

from nova import block_device
from nova import context


class TestContext(unittest.TestCase):
    """ Create Nova context out of Nova source tree


    To create a context for test case using for purpose of reading
    database.
    """
    def test_create_context(self):
        cxt = context.get_context()
        print(cxt)
        self.assertTrue(True)

