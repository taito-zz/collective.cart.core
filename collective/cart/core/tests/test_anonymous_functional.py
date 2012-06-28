from Testing import ZopeTestCase as ztc
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IAddableToCart
from collective.cart.core.interfaces import IProduct
from collective.cart.core.tests.base import FUNCTIONAL_TESTING
from hexagonit.testing.browser import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing import layered
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest2 as unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    self.globs.update({
        'portal': layer['portal'],
        'portal_url': layer['portal'].absolute_url(),
        'browser': Browser(layer['app']),
    })
    ztc.utils.setupCoreSessions(layer['app'])
    portal = self.globs['portal']
    browser = self.globs['browser']
    portal_url = self.globs['portal_url']
    browser.setBaseUrl(portal_url)

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    portal.invokeFactory(
        'CartFolder',
        'cfolder',
    )
    cfolder = portal.cfolder
    cfolder.reindexObject()
    portal.invokeFactory(
        'Document',
        'document01',
        title='Document01',
    )
    document01 = portal.document01
    document01.reindexObject()
    alsoProvides(document01, IAddableToCart)
    IAnnotations(document01)['collective.cart.core'] = ProductAnnotations()
    product01 = IProduct(document01)
    product01.price = 10.0
    product01.stock = 20
    product01.unlimited_stock = False
    product01.max_addable_quantity = 30
    portal.invokeFactory(
        'Document',
        'document02',
        title='Document02',
    )
    document02 = portal.document02
    document02.reindexObject()
    alsoProvides(document02, IAddableToCart)
    IAnnotations(document02)['collective.cart.core'] = ProductAnnotations()
    product02 = IProduct(document02)
    product02.price = 5.0
    product02.unlimited_stock = True

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([
        # DocFileSuite('functional/anonymous_functional.txt'),
        ])
