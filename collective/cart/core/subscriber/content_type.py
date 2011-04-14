from Acquisition import aq_inner, aq_parent
from zope.component import adapter
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.statusmessages.interfaces import IStatusMessage
from Products.Archetypes.interfaces.base import IBaseContent
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.folder import ATFolder
from collective.cart.core import CartMessageFactory as _
from collective.cart.core.interfaces import (
    IAddableToCart,
    ICartFolder,
    IPortalAdapter,
    IPotentiallyAddableToCart,
)

@adapter(ATCTContent, IObjectInitializedEvent)
def addable_to_cart(context, event):
    assert context == event.object
    if context.restrictedTraverse("addable-to-cart")():
        return
    alsoProvides(context, IPotentiallyAddableToCart)
    context.reindexObject()

@adapter(ICartFolder, IObjectInitializedEvent)
def delete_newly_created_cart_folder(context, event):
    assert context == event.object
    catalog = getToolByName(context, 'portal_catalog')
    if len(catalog(object_provides=ICartFolder.__identifier__)) != 1:
#        parent = aq_parent(aq_inner(context))
#        parent.restrictedTraverse("delete-newly-created-cart-folder")()
        context = aq_inner(context)
#        url = context.absolute_url()
#        parent_url = aq_parent(aq_inner(context)).absolute_url()
        putils = getToolByName(context, 'plone_utils')
        paths = ['/'.join(context.getPhysicalPath())]
        putils.deleteObjectsByPaths(paths=paths)
#        message = _(u"You need to delete other CartFolder before adding new CartFolder.")
#        IStatusMessage(context.REQUEST).addStatusMessage(message, type='warn')
#        return self.request.response.redirect(url)
