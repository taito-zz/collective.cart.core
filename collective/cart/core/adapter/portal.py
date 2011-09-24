from Acquisition import aq_chain
from Acquisition import aq_inner
from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.properties import IPropertiesTool
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartContentType
from collective.cart.core.interfaces import ICartFolder
from collective.cart.core.interfaces import ICartFolderContentType
from collective.cart.core.interfaces import IDecimalPlaces
from collective.cart.core.interfaces import IPortal
from collective.cart.core.interfaces import IPortalCartProperties
from collective.cart.core.interfaces import IPrice
from collective.cart.core.interfaces import IPriceWithCurrency
from collective.cart.core.subscriber.event import UpdateCart
from collective.cart.core.subscriber.event import UpdateCartTotal
from zope.component import adapts
from zope.component import getUtility
from zope.event import notify
from zope.interface import implements


class Portal(object):

    adapts(IItem)
    implements(IPortal)

    def __init__(self, context):
        self.context = context
        context = aq_inner(self.context)
        self.catalog = getToolByName(context, 'portal_catalog')
        self.properties = getToolByName(context, 'portal_properties')
        self.sdm = getToolByName(context, 'session_data_manager')
        self.session = self.sdm.getSessionData(create=True)
        self.session_cart_id = self.session.get('collective.cart.core.id')

    @property
    def has_cart_folder(self):
        query = dict(
                object_provides=ICartFolderContentType.__identifier__,
            )
        return self.catalog.unrestrictedSearchResults(query)

    @property
    def cart_folder(self):
        context = aq_inner(self.context)
        chains = [obj for obj in aq_chain(context) if hasattr(obj, 'Type')]
        if len(chains) != 1:
            chains = chains[1:]
        for obj in chains:
            for ob in obj.objectValues():
                if ICartFolderContentType.providedBy(ob):
                    return ob

    @property
    def cart(self):
        if self.session_cart_id is not None:
            path = '/'.join(self.cart_folder.getPhysicalPath())
            query = dict(
                object_provides=ICartContentType.__identifier__,
                session_cart_id=self.session_cart_id,
                path=path,
            )
            brains = self.catalog.unrestrictedSearchResults(query)
            if brains:
                return brains[0].getObject()

    def decimal_price(self, price):
        currency = IPortalCartProperties(self.properties).currency
        places = getUtility(IDecimalPlaces)(currency)
        decimal_price = getUtility(IPrice, name="decimal")
        return decimal_price(price, places)

    def add_to_cart(self, form):
        cart = self.cart
        if cart is None:
            session_cart_id = self.session_cart_id
            if session_cart_id is None:
                idx = [index for index in self.catalog.getIndexObjects() if index.id == 'session_cart_id']
                if idx:
                    session_cart_id = str(idx[0].numObjects() + 1)
                    self.session.set('collective.cart.core.id', session_cart_id)
            cart = ICartFolder(self.cart_folder).create_cart(session_cart_id)
        uid = form.get('uid')
        icart = ICart(cart)
        quantity = int(form.get('quantity'))
        if icart.product(uid):
            icart.add_existing_product_to_cart(uid, quantity)
        else:
            icart.add_new_product_to_cart(uid, quantity)
        notify(UpdateCart(cart))
        notify(UpdateCartTotal(cart))

    def update_cart(self, form):
        if self.cart:
            uid = form.get('uid')
            quantity = int(form.get('quantity'))
            ICart(self.cart).update_cart(uid, quantity)
            notify(UpdateCart(self.cart))
            notify(UpdateCartTotal(self.cart))

    def delete_product(self, form):
        if self.cart:
            uid = form.get('uid')
            ICart(self.cart).delete_product(uid)
            notify(UpdateCart(self.cart))
            notify(UpdateCartTotal(self.cart))

    @property
    def cart_properties(self):
        return IPortalCartProperties(self.properties)


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
        html = '<select id="%s" name="%s">' % (attribute, attribute)
        for lis in lists:
            if lis == value:
                html += '<option value="%s" selected="selected">%s</option>' % (lis, lis)
            else:
                html += '<option value="%s">%s</option>' % (lis, lis)
        html += '</select>'
        return html

    def price_with_currency(self, price):
        symbol = self.currency
        if self.currency_symbol != '':
            symbol = self.currency_symbol
        price = str(price)
        return getUtility(IPriceWithCurrency)(price, self.currency, self.symbol_location, self.decimal_type, symbol)
