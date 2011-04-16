from Acquisition import aq_chain, aq_inner
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts, getMultiAdapter, getUtility
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import (
    IAddableToCart,
    IPortalAdapter,
    IPortalCatalog,
    IPortalCartProperties,
    IPortalSessionCatalog,
    IProduct,
    ISelectRange,
)


class Product(object):
    implements(IProduct)
    adapts(IAddableToCart)

    def __init__(self, context):
        self.context = context

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        else:
            annotations = IAnnotations(self.context)
            if annotations.get('collective.cart.core', None) is None:
                annotations['collective.cart.core'] = ProductAnnotations()
            return getattr(annotations['collective.cart.core'], attr)

    def __setattr__(self, attr, value):
        if attr == 'context':
            self.__dict__[attr] = value
        else:
            annotations = IAnnotations(self.context)
            setattr(annotations['collective.cart.core'], attr, value)

    @property
    def uid(self):
        return self.context.UID()

    @property
    def title(self):
        return self.context.Title()

    @property
    def dimension(self):
        if self.height and self.width and self.depth:
            return float(self.height * self.width * self.depth) / 10 ** 6

    def weight_in_kg(self, ratio=None):
        weight = self.weight
        if self.weight_unit == 'g':
            weight = self.weight / 1000
        if self.dimension and ratio:
            d_weight = self.dimension * ratio
            if d_weight > weight:
                weight = d_weight
        return weight

    @property
    def addable_quantity(self):
        if self.unlimited_stock:
            return self.max_addable_quantity
        else:
            if self.max_addable_quantity > self.stock:
                return self.stock
            else:
                return self.max_addable_quantity

    @property
    def select_quantity(self):
        if self.addable_quantity > 0:
            html = '<select id="quantity" name="quantity">'
            for qtt in getUtility(ISelectRange)(self.addable_quantity):
                html += '<option value="%s">%s</option>' %(qtt,  qtt)
            html += '</select>'
            return html

    @property
    def cart_folder(self):
        context = aq_inner(self.context)
        chain = [obj for obj in aq_chain(context) if hasattr(obj, 'Type')]
        for cha in chain:
            objs = cha.objectValues()
            for obj in objs:
                if obj.meta_type == 'CartFolder':
                    return obj

    def next_cart_id(self, method, digits=1):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        pcatalog = getMultiAdapter((portal, portal.catalog), IPortalCatalog)
        if method == 'Incremental':
            return self.next_incremental_cart_id
        else:
            return pcatalog.random_cart_id(digits)

    def add_to_cart(self, form):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        uid = form.get('uid')
        quantity = int(form.get('quantity'))
        psc = getMultiAdapter((portal, portal.session_data_manager, portal.portal_catalog),IPortalSessionCatalog)
        if psc.cart is not None:
            cart_id = psc.cart_id
        if psc.cart is None:
            properties = IPortalCartProperties(portal.portal_properties)
            method = properties.cart_id_method
            digits = properties.random_cart_id_digits
            method = self.cart_folder.cart_id_numbering_method
            digits = self.cart_folder.random_digits_cart_id
            cart_id = IPortalAdapter(portal).next_cart_id(method, digits)
        getMultiAdapter((portal, portal.session_data_manager, portal.portal_catalog), IPortalSessionCatalog).add_to_cart(uid, quantity, cart_id)

