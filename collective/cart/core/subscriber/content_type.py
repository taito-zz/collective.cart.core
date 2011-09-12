from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.ATContentTypes.content.base import ATCTContent
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import ICartFolderContentType
from collective.cart.core.interfaces import IPotentiallyAddableToCart
from zope.component import adapter
from zope.interface import alsoProvides


@adapter(ATCTContent, IObjectInitializedEvent)
def addable_to_cart(context, event):
    assert context == event.object
    if context.restrictedTraverse("addable-to-cart")():
        return
    alsoProvides(context, IPotentiallyAddableToCart)
    context.reindexObject()


@adapter(ICartFolderContentType, IObjectInitializedEvent)
def delete_old_cart_folder(context, event):
    """Delete Cart Folder in the same hierarchy."""
    assert context == event.object
    catalog = getToolByName(context, 'portal_catalog')
    parent = aq_parent(aq_inner(context))
    path = '/'.join(parent.getPhysicalPath())
    brains = catalog(
        object_provides=ICartFolderContentType.__identifier__,
        path=dict(
            query=path,
            depth=1,
        ),
    )
    objs = [brain.getObject() for brain in brains if brain.UID != context.UID()]
    if objs:
        for obj in objs:
            obj.unindexObject()
            del parent[obj.id]
    ## Make the content language neutral
    if context.getField('language').get(context) != '':
        context.getField('language').set(context, '')
