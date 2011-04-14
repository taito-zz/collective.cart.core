from Acquisition import aq_inner
from zope.component import getMultiAdapter#, getUtility
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cart.core import CartMessageFactory as _
from collective.cart.core.interfaces import (
    ICartAdapter,
    ICartProductOriginal,
    IPortalSessionCatalog,
)


class ICartPortlet(IPortletDataProvider):
    '''A portlet which can render cart content.
    '''


class Assignment(base.Assignment):
    implements(ICartPortlet)

    @property
    def title(self):
        """Title shown in @@manage-portlets.
        """
        return _(u"Cart")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('cart.pt')

#    def update( self ):
#        pass

    @property
    def link_to_cart(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal_url = portal_state.portal_url()
        return '%s/@@cart' % portal_url

    @property
    def available(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('has-cart-contents')()

    def products(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        catalog = getToolByName(portal, 'portal_catalog')
        sdm = getToolByName(portal, 'session_data_manager')
        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
        products = getMultiAdapter((cart, catalog), ICartAdapter).products
        res = []
        for product in products:
            item = dict(
                title = product.title,
                quantity = product.quantity,
                url = getMultiAdapter((product, catalog), ICartProductOriginal).url,
            )
            res.append(item)
        return res


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
