from Acquisition import aq_inner
from zope.publisher.interfaces.browser import IBrowserRequest
try:
    ## Plone4
    from Products.Sessions.interfaces import ISessionDataManager
except ImportError:
    # Plone3
    pass
from zope.component import getUtility, adapts, getMultiAdapter
from zope.interface import implements
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.cart.core.interfaces import (
    IAvailableShippingMethods,
    ICart,
    ICartAdapter,
    ICartFolder,
    ICartProductAdapter,
    IPortalAdapter,
    IPortalCart,
    IPortalCartProperties,
    IPortalCatalog,
    IPortalSession,
    IPortalSessionCatalog,
    IPriceWithCurrency,
    IProduct,
    IRandomDigits,
)
from Products.CMFPlone.interfaces.properties import IPropertiesTool

class PortalCartProperties(object):
    adapts(IPropertiesTool)
    implements(IPortalCartProperties)

    def __init__(self, context):
        self.context = context
        self.properties = getattr(self.context, 'collective_cart_properties')

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        if attr == 'propreties':
            return self.properties
        if attr == 'currency_symbol':
            symbol = self.properties.getProperty('currency_symbol')
            if symbol != '':
                return symbol
            else:
                return self.properties.getProperty('currency')
        else:
            return self.propreties.getProperty(attr)

    def __setattr__(self, attr, value):
        if attr == 'context' or attr == 'properties':
            self.__dict__[attr] = value
        else:
            self.properties._updateProperty(attr, value)

    def select_field(self, attribute, lists):
        value = getattr(self, attribute)
        html = '<select id="%s" name="%s">' %(attribute, attribute)
        for lis in lists:
            if lis == value:
                html += '<option value="%s" selected="selected">%s</option>' %(lis,lis)
            else:
                html += '<option value="%s">%s</option>' %(lis, lis)
        html += '</select>'
        return html

    def price_with_currency(self, price):
        symbol = self.currency
        if self.currency_symbol != '':
            symbol = self.currency_symbol
        return getUtility(IPriceWithCurrency)(price, self.currency, self.symbol_location, self.decimal_type, symbol)

class PortalAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IPortalAdapter)

    def __init__(self, context):
        self.context = context
        self.properties = self.context.portal_properties
        self.catalog = self.context.portal_catalog

    @property
    def cart_properties(self):
        return IPortalCartProperties(self.properties)

    def next_cart_id(self, method, digits=1):
        pcatalog = getMultiAdapter((self.context, self.catalog), IPortalCatalog)
        if method == 'Incremental':
            return pcatalog.incremental_cart_id
        else:
            return pcatalog.random_cart_id(digits)

#    @property
#    def current_cart_products(self):
#        cart = self.current_cart_brain
#        if cart is not None:
#            path = cart.getPath()
#            query = dict(
#            path = path,
##            object_provides = ICartProduct.__identifier__,
#            portal_type = 'CartProduct',
#            )
#            brains = self.catalog.unrestrictedSearchResults(query)
#            if len(brains) != 0:
#                res = []
#                for brain in brains:
#                    obj = brain.getObject()
#                    cpa = ICartProductAdapter(obj)
#                    cpo = getMultiAdapter((obj, self.catalog), ICartProductOriginal)
#                    cpp = getMultiAdapter((obj, self.properties), ICartProductProperties)
#                    item = dict(
#                        uid = cpa.uid,
#                        url = cpo.url,
#                        title = cpa.title,
#                        quantity = cpa.quantity,
#                        price_with_currency = cpp.price_with_currency,
#                        subtotal_price_with_currency = cpp.subtotal_price_with_currency,
#                        select_quantity = cpo.select_quantity,
#                        price = cpa.price,
#                        subtotal = cpa.price * cpa.quantity,
#                    )
#                    res.append(item)
#                return res

    def subtotal_price(self, products):
        prices = [product.get('subtotal') for product in products]
        return sum(prices)

    def shipping_cost(self, products):
        return 0

    def payment_cost(self, products):
        return 0

    def total_cost(self, products):
        price = self.subtotal + self.shipping_cost + self.payment_cost
        return price

    def subtotal_price_with_currency(self, products):
        price = self.subtotal_price(products)
        return IPortalCartProperties(self.properties).price_with_currency(price)

    def shipping_cost_with_currency(self, products):
        price = self.shipping_cost(products)
        return IPortalCartProperties(self.properties).price_with_currency(price)

    def payment_cost_with_currency(self, products):
        price = self.payment_cost(products)
        return IPortalCartProperties(self.properties).price_with_currency(price)


    def total_cost_with_currency(self, products):
        price = self.total_cost(products)
        return IPortalCartProperties(self.properties).price_with_currency(price)

    def product_quantity_in_carts(self, uid):
        brains = self.catalog(
            portal_type='CartProduct',
            review_state='editable_for_customer',
            product_uid=uid,
        )
        quantity = 0
        if len(brains) != 0:
            for brain in brains:
                quantity += brain.product_quantity
        return quantity

#    def update_cart(self, uid, quantity):
#        brain = self.product_brain_in_current_cart(uid)
#        if brain.quantity == quantity:
#            return
#        brains = self.catalog(UID=uid)
#        product = brains[0].getObject()
#        obj = brain.getObject()
#        product = IProduct(product)
#        addable_quantity = product.stock + ICartProductAdapter(obj).quantity
#        if quantity <= addable_quantity:
#            obj.quantity = quantity
#            obj.reindexObject(idxs=['quantity'])
#            new_stock = addable_quantity - quantity
#            product.stock = new_stock
#        else:
#            obj.quantity = updatable_quantity
#            obj.reindexObject(idxs=['quantity'])
#            new_stock = addable_quantity
#            product.getField('cc_stock').set(product, new_stock)

#    def update_cart_from_request(self, request):
#        if IPortalSessionCatalog(self.context, self.sdm, self.catalog).cart is not None:
#            form = request.form
#            uid = form.get('uid')
#            quantity = int(form.get('quantity'))
#            self.update_cart(uid, quantity)

#    def delete_product_from_cart(self, uid, quantity):
#        path = self.product_brain_in_current_cart(uid).getPath()
#        brains = self.catalog(UID=uid)
#        if len(brains) != 0:
#            orig_product = brains[0].getObject()
#            product = IProduct(orig_product)
#            if not product.unlimited_stock:
#                new_stock = product.stock + quantity
#                product.stock = new_stock
#        self.product_brain_in_current_cart(uid).getObject().unindexObject()
#        paths = [path]
#        putils = getToolByName(self.context, 'plone_utils')
#        putils.deleteObjectsByPaths(paths=paths)

class PortalCart(object):
    implements(IPortalCart)
    adapts(IPloneSiteRoot, IBrowserRequest)

    def __init__(self, portal, request):
        self.portal = portal
        self.request = request

    def add_to_cart(self, form):
        form = self.request.form
        uid = form.get('uid')
        quantity = int(form.get('quantity'))
        psc = getMultiAdapter((self.portal, self.portal.session_data_manager, self.portal.portal_catalog),IPortalSessionCatalog)
        if psc.cart is not None:
            cart_id = psc.cart_id
        if psc.cart is None:
            properties = IPortalCartProperties(self.portal.portal_properties)
            method = properties.cart_id_method
            digits = properties.random_cart_id_digits
            cart_id = IPortalAdapter(self.portal).next_cart_id(method, digits)
        getMultiAdapter((self.portal, self.portal.session_data_manager, self.portal.portal_catalog), IPortalSessionCatalog).add_to_cart(uid, quantity, cart_id)

    def update_cart(self):
        catalog = self.portal.portal_catalog
        cart = getMultiAdapter((self.portal, self.portal.session_data_manager, catalog),IPortalSessionCatalog).cart
        if cart is not None:
            form = self.request.form
            uid = form.get('uid')
            quantity = int(form.get('quantity'))
            getMultiAdapter((cart, catalog), ICartAdapter).update_cart(uid, quantity)

    def delete_product_from_cart(self):
        catalog = self.portal.portal_catalog
        cart = getMultiAdapter((self.portal, self.portal.session_data_manager, catalog),IPortalSessionCatalog).cart
        if cart is not None:
            form = self.request.form
            uid = form.get('uid')
            getMultiAdapter((cart, catalog), ICartAdapter).delete_product_from_cart(uid)

class PortalCatalog(object):
    implements(IPortalCatalog)
    adapts(IPloneSiteRoot, IZCatalog)

    def __init__(self, portal, catalog):
        self.portal = portal
        self.catalog = catalog

    @property
    def cart_folder(self):
        query = dict(
            object_provides = ICartFolder.__identifier__,
        )
        brains = self.catalog.unrestrictedSearchResults(query)
        if len(brains) != 0:
            return brains[0].getObject()

    @property
    def used_cart_ids(self):
        query = dict(
            object_provides = ICart.__identifier__,
        )
        brains = self.catalog.unrestrictedSearchResults(query)
        ids = [brain.id for brain in brains]
        return ids

    @property
    def incremental_cart_id(self):
        cart_id = self.cart_folder.next_incremental_cart_id
        while str(cart_id) in self.used_cart_ids:
            cart_id += 1
        new_id = cart_id + 1
        self.cart_folder.next_incremental_cart_id = new_id
        return str(cart_id)

    def random_cart_id(self, digits):
        return getUtility(IRandomDigits)(digits , self.used_cart_ids)

class PortalSession(object):
    implements(IPortalSession)
    try:
        ## Plone4
        adapts(IPloneSiteRoot, ISessionDataManager)
    except NameError:
        ## Plone3
        adapts(IPloneSiteRoot, object)

    def __init__(self, portal, sdm):
        self.portal = portal
        self.sdm = sdm
        self.session = sdm.getSessionData(create=False)
        if self.session is None:
            self.session = sdm.getSessionData(create=True)
        self.cart_id = self.session.get('collective.cart.core.id')

    def delete_cart_id_from_session(self):
        if self.cart_id is not None:
            del self.session['collective.cart.core.id']

class PortalSessionCatalog(object):
    implements(IPortalSessionCatalog)

    try:
        ## Plone4
        adapts(IPloneSiteRoot, ISessionDataManager, IZCatalog)
    except NameError:
        ## Plone3
        adapts(IPloneSiteRoot, object, IZCatalog)

    def __init__(self, portal, sdm, catalog):
        self.portal = portal
        self.sdm = sdm
        self.session = sdm.getSessionData(create=False)
        if self.session is None:
            self.session = sdm.getSessionData(create=True)
        self.cart_id = self.session.get('collective.cart.core.id')
        self.catalog = catalog

    @property
    def cart(self):
        query = dict(
            object_provides = ICart.__identifier__,
            id = self.cart_id,
        )
        brains = self.catalog.unrestrictedSearchResults(query)
        if len(brains) != 0:
            return brains[0].getObject()

    def add_to_cart(self, uid, quantity, cart_id):
        cart = self.cart
        if cart is None:
            self.session.set('collective.cart.core.id', cart_id)
            cfolder = getMultiAdapter((self.portal, self.catalog), IPortalCatalog).cart_folder
            cfolder.invokeFactory(
                'Cart',
                cart_id,
            )
            cart = cfolder[cart_id]
            cart.reindexObject()
        cadapter = getMultiAdapter((cart, self.catalog), ICartAdapter)
        if cadapter.product(uid) is None:
            cadapter.add_new_product_to_cart(uid, quantity)
        else:
            cadapter.add_existing_product_to_cart(uid, quantity)


class AvailableShippingMethods(object):

    adapts(IPloneSiteRoot)
    implements(IAvailableShippingMethods)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return None
