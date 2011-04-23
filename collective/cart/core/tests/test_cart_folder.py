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
        ztc.utils.setupCoreSessions(self.app)
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

        cfolder01 = folder01.cfolder01
        cfolder01.invokeFactory(
            'Cart',
            '0',
            title='0',
        )
        cart00 = cfolder01['0']
        cart00.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '1',
            title='1',
        )
        cart01 = cfolder01['1']
        cart01.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '2',
            title='2',
        )
        cart02 = cfolder01['2']
        cart02.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '3',
            title='3',
        )
        cart03 = cfolder01['3']
        cart03.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '4',
            title='4',
        )
        cart04 = cfolder01['4']
        cart04.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '5',
            title='5',
        )
        cart05 = cfolder01['5']
        cart05.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '7',
            title='7',
        )
        cart07 = cfolder01['7']
        cart07.reindexObject()
        cfolder01.invokeFactory(
            'Cart',
            '8',
            title='8',
        )
        cart08 = cfolder01['8']
        cart08.reindexObject()
#        cfolder01.invokeFactory(
#            'Cart',
#            '5',
#            title='5',
#        )
#        cart05 = cfolder01['5']
#        cart05.reindexObject()



def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'tests/integration/cart_folder.txt', package='collective.cart.core',
            test_class=IntegrationTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
