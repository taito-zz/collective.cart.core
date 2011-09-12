from Acquisition import aq_inner
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartContentType
from collective.cart.core.interfaces import ICartFolder
from collective.cart.core.interfaces import ICartFolderContentType
from collective.cart.core.interfaces import ICartProduct
from collective.cart.core.interfaces import ICartProductContentType
from collective.cart.core.interfaces import IPortal
from collective.cart.core.interfaces import IProduct
from collective.cart.core.interfaces import IRandomDigits
from collective.cart.core.interfaces import ISelectRange
from zope.component import adapts
from zope.component import getUtility
from zope.event import notify
from zope.interface import implements


class CartProductAdapter(object):

    implements(ICartProduct)
    adapts(ICartProductContentType)

    def __init__(self, context):
        self.context = context

    @property
    def uid(self):
        return self.context.uid

    @property
    def title(self):
        return self.context.title

    @property
    def quantity(self):
        return self.context.quantity

    @property
    def price(self):
        return self.context.price

    @property
    def subtotal(self):
        return self.context.subtotal

    @property
    def product(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = dict(UID=self.uid)
        obj = catalog.unrestrictedSearchResults(query)[0].getObject()
        return IProduct(obj)
        # return IProduct(catalog.unrestrictedSearchResults(query)[0].getObject())

    @property
    def max_quantity(self):
        if self.product.unlimited_stock:
            return self.product.max_addable_quantity
        else:
            quantity = self.quantity
            if quantity is None:
                quantity = 0
            total_quantity = quantity + self.product.stock
            if self.product.max_addable_quantity > total_quantity:
                return total_quantity
            else:
                return self.product.max_addable_quantity

    @property
    def select_quantity(self):
        if self.max_quantity > 0:
            html = '<select id="quantity" name="quantity">'
            for qtt in getUtility(ISelectRange)(self.max_quantity):
                if qtt == self.quantity:
                    code = '<option value="%s" selected="selected">%s</option>' % (qtt,  qtt)
                    html += code
                else:
                    html += '<option value="%s">%s</option>' % (qtt, qtt)
            html += '</select>'
            return html

    @property
    def input_quantity(self):
        if self.max_quantity > 0:
            html = '<input type="text "id="quantity" name="quantity" size="3" value="%s" />' % self.quantity
            return html

    @property
    def html_quantity(self):
        context = aq_inner(self.context)
        if IPortal(context).cart_folder.quantity_method == 'Select':
            return self.select_quantity
        else:
            return self.input_quantity


class CartAdapter(object):

    implements(ICart)
    adapts(ICartContentType)

    def __init__(self, context):
        self.context = context

    @property
    def products(self):
        return self.context.objectValues()

    def product(self, uid):
        product = [prod for prod in self.products if prod.uid == uid]
        if product:
            return product[0]

    @property
    def subtotal(self):
        prices = [ICartProduct(product).subtotal for product in self.products]
        return sum(prices)

    @property
    def total_cost(self):
        context = aq_inner(self.context)
        return sum(context.totals.values())

    def add_new_product_to_cart(self, uid, quantity):
        pid = '1'
        if self.products is not None:
            ids = [product.id for product in self.products]
            for r in range(1, len(ids) + 2):
                pid = str(r)
                if pid not in ids:
                    pid = pid
                    break
        self.context.invokeFactory(
            'CartProduct',
            pid,
        )
        cproduct = self.context[pid]
        cproduct.uid = uid
        max_quantity = ICartProduct(cproduct).max_quantity
        if quantity > max_quantity:
            quantity = max_quantity
        cproduct.quantity = quantity
        product = ICartProduct(cproduct).product
        cproduct.price = product.price
        cproduct.title = product.title
        cproduct.subtotal = cproduct.price * cproduct.quantity
        cproduct.reindexObject()
        if not product.unlimited_stock:
            new_stock = product.stock - quantity
            product.stock = new_stock
        notify(ObjectInitializedEvent(cproduct))

    def add_existing_product_to_cart(self, uid, quantity):
            cproduct = self.product(uid)
            product = ICartProduct(cproduct).product
            total_quantity = product.stock + cproduct.quantity
            max_quantity = ICartProduct(cproduct).max_quantity
            new_quantity = cproduct.quantity + quantity
            if new_quantity > max_quantity:
                new_quantity = max_quantity
            cproduct.quantity = new_quantity
            cproduct.subtotal = cproduct.price * cproduct.quantity
            cproduct.reindexObject(idxs=['quantity'])
            product = ICartProduct(cproduct).product
            if not product.unlimited_stock:
                new_stock = total_quantity - new_quantity
                product.stock = new_stock

    def update_cart(self, uid, quantity):
        cproduct = self.product(uid)
        icp = ICartProduct(cproduct)
        product = icp.product
        if product.unlimited_stock:
            if quantity > product.max_addable_quantity:
                quantity = product.max_addable_quantity
            cproduct.quantity = quantity
            cproduct.reindexObject(idxs=['quantity'])
        else:
            total_quantity = cproduct.quantity + product.stock
            if quantity <= icp.max_quantity:
                cproduct.quantity = quantity
            else:
                cproduct.quantity = icp.max_quantity
            cproduct.reindexObject(idxs=['quantity'])
            new_stock = total_quantity - cproduct.quantity
            product.stock = new_stock
        cproduct.subtotal = cproduct.price * cproduct.quantity

    def delete_product(self, uid):
        cproduct = self.product(uid)
        quantity = cproduct.quantity
        product = ICartProduct(cproduct).product
        if not product.unlimited_stock:
            new_stock = product.stock + quantity
            product.stock = new_stock
        cproduct.unindexObject()
        del self.context[cproduct.id]


class CartFolderAdapter(object):

    adapts(ICartFolderContentType)
    implements(ICartFolder)

    def __init__(self, context):
        self.context = context
        context = aq_inner(self.context)
        self.catalog = getToolByName(context, 'portal_catalog')

    @property
    def used_cart_ids(self):
        context = aq_inner(self.context)
        path = '/'.join(context.getPhysicalPath())
        query = dict(
            object_provides=ICartContentType.__identifier__,
            path=path,
        )
        brains = self.catalog.unrestrictedSearchResults(query)
        ids = [brain.id for brain in brains]
        return ids

    @property
    def incremental_cart_id(self):
        cart_id = self.context.next_incremental_cart_id
        while str(cart_id) in self.used_cart_ids:
            cart_id += 1
        new_id = cart_id + 1
        self.context.next_incremental_cart_id = new_id
        return str(cart_id)

    @property
    def random_cart_id(self):
        digits = self.context.random_digits_cart_id
        if digits is None:
            digits = 1
        while len([uci for uci in self.used_cart_ids if len(uci) == digits]) == 10 ** digits:
            digits += 1
            self.context.random_digits_cart_id = digits
        return getUtility(IRandomDigits)(digits, [uci for uci in self.used_cart_ids if len(uci) == digits])

    @property
    def next_cart_id(self):
        if self.context.cart_id_numbering_method == 'Incremental':
            return self.incremental_cart_id
        else:
            return self.random_cart_id

    def create_cart(self, session_cart_id):
        cart_id = self.next_cart_id
        self.context.invokeFactory(
            'Cart',
            cart_id,
            title=cart_id,
        )
        cart = self.context[cart_id]
        cart.session_cart_id = session_cart_id
        notify(ObjectInitializedEvent(cart))
        cart.reindexObject()
        return cart
