try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest
from Testing import ZopeTestCase as ztc
from collective.cart.core.tests import base

from zope.interface import alsoProvides
from collective.cart.core.interfaces import IAddableToCart


class IntegrationTestCase(base.TestCase):
    """Base class used for test cases
    """

    def afterSetUp( self ):
        """Code that is needed is the afterSetUp of both test cases.
        """
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Folder', 'folder01')
        folder01 = self.portal.folder01
        self.portal.invokeFactory('Folder', 'folder02')
        folder02 = self.portal.folder02
        folder01.invokeFactory('Folder', 'folder03')
        folder03 = folder01.folder03
        folder03.invokeFactory('Folder', 'folder04')
        folder04 = folder03.folder04
        folder04.invokeFactory('Folder', 'folder05')
        folder05 = folder04.folder05
        folder05.invokeFactory('CartFolder', 'cfolder05')
        folder04.invokeFactory('CartFolder', 'cfolder04')
        folder04.invokeFactory('Document', 'doc01')
        doc01 = folder04.doc01
        alsoProvides(doc01, IAddableToCart)
        folder03.invokeFactory('CartFolder', 'cfolder03')
        folder02.invokeFactory('CartFolder', 'cfolder02')
        folder01.invokeFactory('CartFolder', 'cfolder01')

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'tests/integration/cart_folder.txt', package='collective.cart.core',
            test_class=IntegrationTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
