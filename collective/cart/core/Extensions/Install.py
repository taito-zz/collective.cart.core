from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

EXTENSION_PROFILES = ('collective.cart.core:uninstall',)


def uninstall(self):
    out = StringIO()
    print >> out, "Removing collective.cart.core"

    controlpanel = getToolByName(self, 'portal_controlpanel')
    actids = [o.id for o in controlpanel.listActions()]
    controlpanel.deleteActions([actids.index('collective_cart_config')])

    properties = getToolByName(self, 'portal_properties')
    properties.manage_delObjects(ids=['collective_cart_properties'])

    setup = getToolByName(self, 'portal_setup')
    for extension_id in EXTENSION_PROFILES:
        profile = 'profile-%s' % extension_id
        setup.runAllImportStepsFromProfile(
            profile,
            purge_old=False,
        )

    return out.getvalue()
