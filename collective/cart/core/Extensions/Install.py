from StringIO import StringIO
from zope.annotation.interfaces import IAnnotations
from zope.component import getSiteManager
from Products.CMFCore.utils import getToolByName


def uninstall(self):
    out = StringIO()
    print >> out, "Removing collective.cart.core"

    controlpanel = getToolByName(self, 'portal_controlpanel')
    actids = [o.id for o in controlpanel.listActions()]
    controlpanel.deleteActions([actids.index('collective_cart_config')])

    properties = getToolByName(self, 'portal_properties')
    properties.manage_delObjects(ids=['collective_cart_properties'])

    return out.getvalue()
