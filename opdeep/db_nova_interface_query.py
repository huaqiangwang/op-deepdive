import unittest
# Check if failed in loading nova modules then doing following two steps
import sys
sys.path.append('/opt/stack/nova')

from nova import block_device
from nova import context
from nova import objects

from nova.objects.instance import InstanceList
from nova.compute import api


class TestContext(unittest.TestCase):
    """ Create Nova context out of Nova source tree

    To create a context for test case using for purpose of reading
    database.
    """
    def setUp(self) -> None:
        objects.register_all()

    def test_create_context(self):
        cxt = context.get_admin_context()
        print(cxt)
        self.assertIsNotNone(cxt)

    def test_intstance_get_all(self):
        """ Attempt to access Nova objects and get real on node data.

        These are attempts to retrieve nova node data through 'nova'
        project objects and methods, not APIs. It failed by gettig errors
        such as 'no such table: cell_mapping', the reason I believe is due to
        lack of proper DB engine session, I probably used wrong context
        and its DB engine is not initialized correctly, how are the
        OS_AUTH, OS_PROJECT_NAME, OS_USER_NAME environments properly
        handled to create a session referring to a proper nova controller?

        It's not a good way to do so, the Nova source code defined method and
        objects are not intent for out source code user using, evidence is
        you even need to call 'object.resgister_all()' after 'from nova import
        objects', all these are not standard OPs for importing a python module.
        """
        cxt = context.get_admin_context()
        api.load_cells()
        '''
        list = InstanceList()
        list.get_all(cxt)
        print(list)
        '''
        # Do not using this way for inspecting nova node data, using standing APIs
        # or extent the 'nova' project itself.
        self.assertTrue(False)

