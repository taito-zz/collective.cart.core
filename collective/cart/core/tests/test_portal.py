try:
    import unittest2 as unittest
except ImportError:
    import unittest
#import doctest
from doctest import (
    ELLIPSIS,
    NORMALIZE_WHITESPACE,
    REPORT_ONLY_FIRST_FAILURE
)
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from collective.cart.core.tests import base

OF = ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_ONLY_FIRST_FAILURE

class TestCase(base.TestCase):
    """Base class used for test cases
    """

    def afterSetUp( self ):
        """Code that is needed is the afterSetUp of both test cases.
        """
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        self.setRoles(('Manager',))
        wftool = getToolByName(self.portal, 'portal_workflow')
        self.portal.invokeFactory(
            'Document',
            'doc01',
            title='Document01',
            description='Description of Document01',
        )
        doc01 = self.portal.doc01
        wftool.doActionFor(doc01, "publish")
        doc01.reindexObject()
        self.portal.invokeFactory(
            'CartFolder',
            'cfolder',
        )
        cfolder = self.portal.cfolder
        cfolder.invokeFactory(
            'Cart',
            '1',
        )
        cart01 = cfolder['1']
        cart01.session_cart_id = '1'
        cart01.reindexObject()

def test_suite():
    return unittest.TestSuite(
        [

            # Integration tests for Content Types.
            ztc.ZopeDocFileSuite(
                'tests/integration/portal.txt',
                package='collective.cart.core',
                test_class=TestCase,
                optionflags=OF
            ),

        ]
    )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
