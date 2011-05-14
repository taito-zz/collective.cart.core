from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
#from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cart.core import CartMessageFactory as _
#from collective.cart.core.interfaces import (
#    ICartProduct,
#    IPortalSessionCatalog,
#)


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

    @property
    def link_to_cart(self):
#        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
#        portal_url = portal_state.portal_url()
#        return '%s/@@cart' % portal_url
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        url = context_state.object_url()
        return '%s/@@cart' % url

    @property
    def available(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('products')()

    def products(self):
        return self.available


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
