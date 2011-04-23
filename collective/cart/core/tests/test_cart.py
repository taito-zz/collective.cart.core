try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest
from Testing import ZopeTestCase as ztc
from collective.cart.core.tests import base

from decimal import Decimal
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IAddableToCart, IProduct


class IntegrationTestCase(base.TestCase):
    """Base class used for test cases
    """

    def afterSetUp( self ):
        """Code that is needed is the afterSetUp of both test cases.
        """
        ztc.utils.setupCoreSessions(self.app)
        self.setRoles(('Manager',))
        wftool = getToolByName(self.portal, 'portal_workflow')
        self.portal.invokeFactory('CartFolder', 'cfolder')
#        cfolder = self.portal.cfolder

        ## Create Product00
        self.portal.invokeFactory(
            'Document',
            'doc00',
            title='Product00',
            description='Description of Product00',
        )
        doc00 = self.portal.doc00
        wftool.doActionFor(doc00, "publish")
        alsoProvides(doc00, IAddableToCart)
        IAnnotations(doc00)['collective.cart.core'] = ProductAnnotations()
        product00 = IProduct(doc00)
        product00.price = Decimal('100.00')
        product00.unlimited_stock = True
        product00.max_addable_quantity = 5

        ## Create Product01
        self.portal.invokeFactory(
            'Document',
            'doc01',
            title='Product01',
            description='Description of Product01',
        )
        doc01 = self.portal.doc01
        wftool.doActionFor(doc01, "publish")
        alsoProvides(doc01, IAddableToCart)
        IAnnotations(doc01)['collective.cart.core'] = ProductAnnotations()
        product01 = IProduct(doc01)
        product01.price = Decimal('10.00')
        product01.stock = 50
        product01.max_addable_quantity = 30

        ## Create Product02
        self.portal.invokeFactory(
            'Document',
            'doc02',
            title='Product02',
            description='Description of Product02',
        )
        doc02 = self.portal.doc02
        wftool.doActionFor(doc02, "publish")
        alsoProvides(doc02, IAddableToCart)
        IAnnotations(doc02)['collective.cart.core'] = ProductAnnotations()
        product02 = IProduct(doc02)
        product02.price = Decimal('5.00')
        product02.stock = 20
        product02.max_addable_quantity = 50



def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'tests/integration/cart.txt', package='collective.cart.core',
            test_class=IntegrationTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
