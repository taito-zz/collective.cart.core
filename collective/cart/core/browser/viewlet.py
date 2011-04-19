from zope.component import getMultiAdapter, getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import alsoProvides, noLongerProvides
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from collective.cart.core.interfaces import (
    IAddableToCart,
    ICartAdapter,
    ICartItself,
    ICartProductAdapter,
    ICartProductOriginal,
    IPortalAdapter,
    IPortalCart,
    IPortalCartProperties,
    IPortalCatalog,
    IPortalSessionCatalog,
    IPotentiallyAddableToCart,
    IProduct,
)


class CartViewletBase(ViewletBase):

    @property
    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_context_state')
        return context_state.current_page_url()

class CartConfigPropertiesViewlet(CartViewletBase):
    """Properties Viewlet for Cart Config."""

    index = render = ViewPageTemplateFile("viewlets/cart_properties.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdateCartProperties', None) is not None:
            context = aq_inner(self.context)
            keys = form.keys()
            keys.remove('form.button.UpdateCartProperties')
            ## Ther order matters here.
            keys.sort()
            for key in keys:
                setattr(IPortalAdapter(context).cart_properties, key, form.get(key))

    def selects(self):
        names = ['currency', 'symbol_location', 'decimal_type']
        html = ''
        for name in names:
            html += getattr(self, name)
        return html

    @property
    def currency(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.select_field('currency', ['EUR', 'USD', 'JPY'])

    @property
    def currency_symbol(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.currency_symbol

    @property
    def symbol_location(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.select_field('symbol_location', ['Front', 'Behind'])

    @property
    def decimal_type(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.select_field('decimal_type', ['.', ','])

    @property
    def cart_id_method(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.select_field('cart_id_method', ['Incremental', 'Random'])

    @property
    def next_cart_id(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        catalog = getToolByName(context, 'portal_catalog')
        cfolder = getMultiAdapter((portal, catalog), IPortalCatalog).cart_folder
        if cfolder is not None:
            return cfolder.next_incremental_cart_id
        else:
            return 1

    @property
    def random_cart_id_digits(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.random_cart_id_digits

    @property
    def quantity_method(self):
        context = aq_inner(self.context)
        return IPortalAdapter(context).cart_properties.select_field('quantity_method', ['Select', 'Input'])


class CartConfigTypesViewlet(CartViewletBase):
    """Content Type Selection Viewlet for Cart Config."""

    index = render = ViewPageTemplateFile("viewlets/cart_types.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdateContentTypes', None) is not None:
            types = form.get('types', None)
            if types is not None:
                if type(types).__name__ == 'str':
                    types = [types]
                context = aq_inner(self.context)
                portal = getToolByName(context, 'portal_url').getPortalObject()
                IPortalAdapter(portal).cart_properties.content_types = types
                catalog = getToolByName(context, 'portal_catalog')
                brains = catalog(
                    portal_type=types,
                )
                if len(brains) != 0:
                    for brain in brains:
                        obj = brain.getObject()
                        if not IPotentiallyAddableToCart.providedBy(obj):
                            alsoProvides(obj, IPotentiallyAddableToCart)
                addables = catalog(
                    object_provides = IAddableToCart.__identifier__,
                )
                objs = [ad.getObject() for ad in addables if ad in brains]
                if len(objs) != 0:
                    for obj in objs:
                        noLongerProvides(obj, [IAddableToCart, IPotentiallyAddableToCart])

    def select_types(self):
        context = aq_inner(self.context)
        sct = IPortalAdapter(context).cart_properties.content_types
        name = 'plone.app.vocabularies.UserFriendlyTypes'
        util = getUtility(IVocabularyFactory, name)
        types = util(context).by_token.keys()
        html = '<select id="types" name="types" size="5" multiple="multiple">'
        for typ in types:
            if sct is not None and typ in sct:
                html += '<option value="%s" selected="selected">%s</option>' %(typ, typ)
            else:
                html += '<option value="%s">%s</option>' %(typ, typ)
        html += '</select>'
        return html


class CartProductValuesViewlet(CartViewletBase):
    """Product Values Viewlet for Content Types."""

    index = render = ViewPageTemplateFile("viewlets/product_values.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.AddToCart', None) is not None:
            context = aq_inner(self.context)
            IProduct(context).add_to_cart(form)
            return self.request.response.redirect(self.current_url) 

    def items(self):
        context = aq_inner(self.context)
        properties = getToolByName(context, 'portal_properties')
        pcp = IPortalCartProperties(properties)
        product = IProduct(context)
        res = dict(
            uid = product.uid,
            select_quantity = product.select_quantity,
            price_with_currency = pcp.price_with_currency(product.price),
        )
        return res


class CartContentsViewlet(CartViewletBase):

    index = render = ViewPageTemplateFile("viewlets/cart_content.pt")

    def update(self):
        form = self.request.form
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        if form.get('form.button.UpdateCartContent', None) is not None:
            getMultiAdapter((portal, self.request), IPortalCart).update_cart()
            return self.request.response.redirect(self.current_url)
        if form.get('form.button.DeleteCartContent', None) is not None:
            getMultiAdapter((portal, self.request), IPortalCart).delete_product_from_cart()
            return self.request.response.redirect(self.current_url)

    @property
    def products(self):
        return self.context.restrictedTraverse('products')()
#        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
#        portal = portal_state.portal()
#        catalog = getToolByName(portal, 'portal_catalog')
#        sdm = getToolByName(portal, 'session_data_manager')
#        properties = getToolByName(portal, 'portal_properties')
#        pcp = IPortalCartProperties(properties)
#        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
#        products = getMultiAdapter((cart, catalog), ICartAdapter).products
#        if products is not None:
#            res = []
#            for product in products:
#                cpo = getMultiAdapter((product, catalog), ICartProductOriginal)
#                cpa = ICartProductAdapter(product)
#                item = dict(
#                    title = cpa.title,
#                    quantity = cpa.quantity,
#                    uid = cpa.uid,
#                    url = cpo.url,
#                    select_quantity = cpo.select_quantity,
#                    price_with_currency = pcp.price_with_currency(cpa.price),
#                    subtotal_with_currency = pcp.price_with_currency(cpa.subtotal),
#                )
#                res.append(item)
#            return res

    def totals_with_currency(self):
        return self.context.restrictedTraverse('totals-with-currency')()
#        if self.products is not None:
#            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
#            portal = portal_state.portal()
#            catalog = getToolByName(portal, 'portal_catalog')
#            sdm = getToolByName(portal, 'session_data_manager')
#            properties = getToolByName(portal, 'portal_properties')
#            pcp = IPortalCartProperties(properties)
#            cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
#            ca = getMultiAdapter((cart, catalog), ICartAdapter)
#            ci = ICartItself(cart)
#            shipping_cost_with_currency = pcp.price_with_currency(ci.shipping_cost)
#            if ci.shipping_cost == 0:
#                shipping_cost_with_currency = None
#            payment_cost_with_currency = pcp.price_with_currency(ca.payment_cost)
#            if ca.payment_cost == 0:
#                payment_cost_with_currency = None
#            data = dict(
#                products_subtotal_with_currency = pcp.price_with_currency(ca.subtotal),
#                shipping_cost_with_currency = shipping_cost_with_currency,
#                payment_cost_with_currency = payment_cost_with_currency,
#                total_cost_with_currency = pcp.price_with_currency(ca.total_cost),
#            )
#            return data


class NextStepViewlet(CartViewletBase):

    index = render = ViewPageTemplateFile("viewlets/cart_next.pt")

    def update(self):
        form = self.request.form
        context = aq_inner(self.context)
        if form.get('form.button.NextStep', None) is not None:
            return context.restrictedTraverse('next-step')()

class FixedInfoViewlet(CartViewletBase):

    index = render = ViewPageTemplateFile("viewlets/fixed_info.pt")

    def has_cart_contents(self):
        return self.context.restrictedTraverse('has-cart-contents')()

class FixedCartContentViewlet(CartContentsViewlet):

    index = render = ViewPageTemplateFile("viewlets/fixed_cart_content.pt")

    def update(self):
        if self.products is None:
            context = aq_inner(self.context)
            portal = getToolByName(context, 'portal_url').getPortalObject()
            portal_url = portal.absolute_url()
            cart_url = '%s/@@cart' % portal_url
            return self.request.response.redirect(cart_url)

    @property
    def products(self):
        products = self.context.restrictedTraverse('has-cart-contents')()
        if products is not None:
            res = []
            context = aq_inner(self.context)
            catalog = getToolByName(context, 'portal_catalog')
            portal = getToolByName(context, 'portal_url').getPortalObject()
            properties = getToolByName(portal, 'portal_properties')
            pcp = IPortalCartProperties(properties)
            for product in products:
                cpo = getMultiAdapter((product, catalog), ICartProductOriginal)
                cpa = ICartProductAdapter(product)
                item = dict(
                    title = cpa.title,
                    quantity = cpa.quantity,
                    uid = cpa.uid,
                    url = cpo.url,
                    price_with_currency = pcp.price_with_currency(cpa.price),
                    subtotal_with_currency = pcp.price_with_currency(cpa.subtotal),
                )
                res.append(item)
            return res

    def totals_with_currency(self):
        if self.products is not None:
            return self.context.restrictedTraverse('totals-with-currency')()

#    index = render = ViewPageTemplateFile("viewlets/fc.pt")
