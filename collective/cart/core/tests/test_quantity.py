import unittest
import doctest
from Testing import ZopeTestCase as ztc
from collective.cart.core.tests import base

from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IAddableToCart, IProduct

class TestSetup(base.FunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        wftool = getToolByName(self.portal, 'portal_workflow')
        self.portal
        self.portal.invokeFactory(
            'CartFolder',
            'cfolder',
            title="Cart Folder",
        )
        cfolder = self.portal.cfolder
        cfolder.reindexObject()
        self.portal.invokeFactory(
            'Document',
            'doc01',
            title='Product01',
        )
        doc01 = self.portal.doc01
        wftool.doActionFor(doc01, "publish")
        doc01.reindexObject()
        alsoProvides(doc01, IAddableToCart)
        IAnnotations(doc01)['collective.cart.core'] = ProductAnnotations()
        product01 = IProduct(doc01)
        product01.price = 10.0
        product01.stock = 10
        product01.unlimited_stock = False
        product01.max_addable_quantity = 20

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/quantity.txt',
            package='collective.cart.core',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
