from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IAddableToCart
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartAware
from collective.cart.core.interfaces import ICartProduct
from collective.cart.core.interfaces import IPortal
from collective.cart.core.interfaces import IPortalCartProperties
from collective.cart.core.interfaces import IPotentiallyAddableToCart
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


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
            url = '%s/@@edit-product' % context.absolute_url()
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
                        uid=product.uid,
                        title=product.title,
                        quantity=product.quantity,
                        url=cproduct.product.url,
                        price_with_currency=pcp.price_with_currency(cproduct.price),
                        html_quantity=cproduct.html_quantity,
                        subtotal_with_currency=pcp.price_with_currency(cproduct.subtotal),
                    )
                    res.append(item)
                return res

    def cart_id(self):
        context = aq_inner(self.context)
        cart = IPortal(context).cart
        if cart:
            return cart.id

    def set_info(self, items):
        context = aq_inner(self.context)
        IPortal(context).cart.info = items

    def total_cost(self):
        context = aq_inner(self.context)
        cart = IPortal(context).cart
        if cart:
            return str(ICart(cart).total_cost)

    def next_step(self):
        context = aq_inner(self.context)
        cfolder = IPortal(context).cart_folder
        form = cfolder.getNext_form()
        if form is not None:
            self.request.response.redirect(form.absolute_url())
        else:
            context.restrictedTraverse('test-step')

    def test_step(self):
        """Method to provide test step."""

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
