from collective.cart.core.tests.base import FUNCTIONAL_TESTING
from leo.testing.browser import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import layered
from zope.testing import renormalizing
from datetime import datetime
from PIL import Image

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
    # Update global variables within the tests.
#     width = 450
#     height = 450
#     black = (0, 0, 0)
#     image = Image.new("RGB", (width, height), black)
#     filename = 'dummy.png'
#     image.save(filename)
    self.globs.update({
        'portal': layer['portal'],
        'portal_url': layer['portal'].absolute_url(),
        'browser': Browser(layer['app']),
        # 'TEST_IMAGE': filename,
    })

    portal = self.globs['portal']
    browser = self.globs['browser']
    portal_url = self.globs['portal_url']
    browser.setBaseUrl(portal_url)

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    portal.invokeFactory(
        'Document',
        'document01',
        title='Document01'
    )
    portal.document01.reindexObject()

    # portal.invokeFactory(
    #         'Document',
    #         'doc01',
    #         title='Style01',
    #         description="Description of Style01",
    #         subject=(
    #             'leo.artwork.style',
    #             'leo.artwork.media',
    #             'leo.artwork.technique',
    #             'leo.artwork.surface',
    #         ),
    #     )
    # doc01 = portal.doc01
    # doc01.reindexObject()
    # self.globs.update({'doc_uid': doc01.UID()})
    # year = str(datetime.now().year)
    # self.globs.update({'current_year': year})

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
        DocFileSuite('functional/content.txt'),
        DocFileSuite('functional/setup_functional.txt'),
        ])