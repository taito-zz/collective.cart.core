from Acquisition import aq_inner, aq_parent
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter#, getUtility
from zope.interface import alsoProvides, noLongerProvides
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import (
    IAddableToCart,
    ICart,
    ICartAware,
    ICartProduct,
    IPortal,
    IPortalCartProperties,
    IPortalCatalog,
    IPortalSessionCatalog,
    IPotentiallyAddableToCart,
#    IPriceInString,
)

class Miscellaneous(BrowserView):

    def potentially_addable_but_not_addable_to_cart(self):
        context = aq_inner(self.context)
        return IPotentiallyAddableToCart.providedBy(context) and not IAddableToCart.providedBy(context)

    def addable_to_cart(self):
        context = aq_inner(self.context)
        return IPotentiallyAddableToCart.providedBy(context) and IAddableToCart.providedBy(context)

    def make_addable_to_cart(self):
        context = aq_inner(self.context)
        if IPotentiallyAddableToCart.providedBy(context):
            alsoProvides(context, IAddableToCart)
            url = '%s/@@edit-product' %context.absolute_url()
            IAnnotations(context)['collective.cart.core'] = ProductAnnotations()
            return self.request.response.redirect(url)

    def make_not_addable_to_cart(self):
        context = aq_inner(self.context)
        noLongerProvides(context, IAddableToCart)
        url = context.absolute_url()
        del IAnnotations(context)['collective.cart.core']
        return self.request.response.redirect(url)

    def products(self):
        context = aq_inner(self.context)
        cart = IPortal(context).cart
        if cart is not None:
            products = ICart(cart).products
            if products:
                properties = getToolByName(context, 'portal_properties')
                pcp = IPortalCartProperties(properties)
                res = []
                for product in products:
                    cproduct = ICartProduct(product)
                    item = dict(
                        uid = product.uid,
                        title = product.title,
                        quantity = product.quantity,
                        url = cproduct.product.url,
                        price_with_currency = pcp.price_with_currency(cproduct.price),
                        html_quantity = cproduct.html_quantity,
                        subtotal_with_currency = pcp.price_with_currency(cproduct.subtotal),
                    )
                    res.append(item)
                return res

    def totals(self):
        if self.products():
            context = aq_inner(self.context)
            cart = IPortal(context).cart
            icart = ICart(cart)
            properties = getToolByName(context, 'portal_properties')
            pcp = IPortalCartProperties(properties)
            data = dict(
                products_subtotal = icart.subtotal,
                products_subtotal_with_currency = pcp.price_with_currency(icart.subtotal),
                total_cost = icart.total_cost,
                total_cost_with_currency = pcp.price_with_currency(icart.total_cost),
            )
            return data


    def cart_id(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sdm = getToolByName(portal, 'session_data_manager')
        catalog = getToolByName(portal, 'portal_catalog')
        return getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart_id

    def total_price(self):
        return self.totals['total_cost']
#        context = aq_inner(self.context)
#        portal = getToolByName(context, 'portal_url').getPortalObject()
#        sdm = getToolByName(portal, 'session_data_manager')
#        catalog = getToolByName(portal, 'portal_catalog')
#        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
#        if cart is not None:
#            price = getMultiAdapter((cart, catalog), ICartAdapter).total_cost
#            pis = getUtility(IPriceInString)
#            return pis(price)

    def next_step(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        catalog = getToolByName(portal, 'portal_catalog')
        cfolder = getMultiAdapter((portal, catalog), IPortalCatalog).cart_folder
        form = cfolder.getNext_form()
        if form is not None:
            self.request.response.redirect(form.absolute_url())
        else:
            context.restrictedTraverse('test-step')

    def test_step(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        catalog = getToolByName(portal, 'portal_catalog')

    def make_cart_aware(self):
        context = aq_inner(self.context)
        alsoProvides(context, ICartAware)
        parent = aq_parent(context)
        alsoProvides(parent, ICartAware)
        url = context.absolute_url()
        return self.request.response.redirect(url)

    def make_not_cart_aware(self):
        context = aq_inner(self.context)
        noLongerProvides(context, ICartAware)
        parent = aq_parent(context)
        noLongerProvides(parent, ICartAware)
        url = context.absolute_url()
        return self.request.response.redirect(url)

    def is_cart_aware(self):
        context = aq_inner(self.context)
        return ICartAware.providedBy(context)

