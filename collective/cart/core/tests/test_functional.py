import unittest
import doctest
from Testing import ZopeTestCase as ztc
from collective.cart.core.tests import base

class TestSetup(base.FunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        self.portal.invokeFactory(
            'Document',
            'document01',
            title='Document01'
        )
        document01 = self.portal.document01
        document01.reindexObject()

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/setup_functional.txt',
            package='collective.cart.core',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
