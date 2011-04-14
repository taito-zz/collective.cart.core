import unittest
import doctest
from Testing import ZopeTestCase as ztc
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from collective.cart.core.tests import base
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
        )
        cfolder = self.portal.cfolder
        cfolder.reindexObject()
        self.portal.invokeFactory(
            'Document',
            'document01',
            title='Document01',
        )
        document01 = self.portal.document01
        wftool.doActionFor(document01, "publish")
        document01.reindexObject()
        alsoProvides(document01, IAddableToCart)
        IAnnotations(document01)['collective.cart.core'] = ProductAnnotations()
        product01 = IProduct(document01)
        product01.price = 10.0
        product01.stock = 20
        product01.unlimited_stock = False
        product01.max_addable_quantity = 30
        self.portal.invokeFactory(
            'Document',
            'document02',
            title='Document02',
        )
        document02 = self.portal.document02
        wftool.doActionFor(document02, "publish")
        document02.reindexObject()
        alsoProvides(document02, IAddableToCart)
        IAnnotations(document02)['collective.cart.core'] = ProductAnnotations()
        product02 = IProduct(document02)
        product02.price = 5.0
        product02.unlimited_stock = True


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/anonymous_functional.txt',
            package='collective.cart.core',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
