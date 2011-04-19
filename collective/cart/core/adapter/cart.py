from Acquisition import aq_inner
from zope.interface import implements
from zope.component import adapts, getUtility, getMultiAdapter
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFCore.utils import getToolByName
from collective.cart.core.content import CartProduct
from collective.cart.core.interfaces import (
    ICart,
    ICartItself,
    ICartAdapter,
    ICartProduct,
    ICartProductAdapter,
    ICartProductOriginal,
    IProduct,
    ISelectRange,
    IShippingCost,
)


class CartProductAdapter(object):

    implements(ICartProductAdapter)
    adapts(CartProduct)

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
        return self.price * self.quantity

class CartProductOriginal(object):
    implements(ICartProductOriginal)
    adapts(ICartProduct, IZCatalog)

    def __init__(self, context, catalog):
        self.context = context
        self.catalog = catalog

    @property
    def brain(self):
        query = dict(UID=self.context.uid)
        return self.catalog.unrestrictedSearchResults(query)[0]

    @property
    def obj(self):
        return self.brain.getObject()

    @property
    def url(self):
        return self.brain.getURL()

    @property
    def updatable_quantity(self):
        product = IProduct(self.obj)
        if product.unlimited_stock:
            return product.max_addable_quantity
        else:
            addable_quantity = product.stock + self.context.quantity
            if product.max_addable_quantity > addable_quantity:
                return addable_quantity
            else:
                return product.max_addable_quantity

    @property
    def select_quantity(self):
        html = '<select id="quantity" name="quantity">'
        for qtt in getUtility(ISelectRange)(self.updatable_quantity):
            if qtt == self.context.quantity:
                code = '<option value="%s" selected="selected">%s</option>' % (qtt,  qtt)
                html += code
            else:
                html += '<option value="%s">%s</option>' %(qtt,  qtt)
        html += '</select>'
        return html

class CartAdapter(object):
    implements(ICartAdapter)
    adapts(ICart, IZCatalog)

    def __init__(self, context, catalog):
        self.context = context
        self.catalog = catalog

    @property
    def products(self):
        context = aq_inner(self.context)
        path = '/'.join(context.getPhysicalPath())
        query = dict(
            path = path,
            object_provides = ICartProduct.__identifier__,
        )
        brains = self.catalog.unrestrictedSearchResults(query)
        if len(brains) != 0:
            objs = [brain.getObject() for brain in brains]
            return objs

    def product(self, uid):
        context = aq_inner(self.context)
        path = '/'.join(context.getPhysicalPath())
        query = dict(
            path=path,
            uid=uid,
        )
        brains = self.catalog.unrestrictedSearchResults(query)
        if len(brains) != 0:
            return brains[0].getObject()

    @property
    def subtotal(self):
        prices = [ICartProductAdapter(product).subtotal for product in self.products]
        return sum(prices)

    @property
    def payment_cost(self):
        return 0

    @property
    def total_cost(self):
        total = self.subtotal + ICartItself(self.context).shipping_cost + self.payment_cost
        return total

    def add_new_product_to_cart(self, uid, quantity):
        pid = '1'
        if self.products is not None:
                pid = str(len(self.products) + 1)
        self.context.invokeFactory(
            'CartProduct',
            pid,
            uid=uid,
        )
        cproduct = self.context[pid]
        cproduct.reindexObject()
        original = getMultiAdapter((cproduct, self.catalog), ICartProductOriginal)
        cproduct.quantity=quantity
        product = IProduct(original.obj)
        cproduct.price=product.price
        cproduct.title=product.title
        cproduct.weight = product.weight
        cproduct.weight_unit = product.weight_unit
        cproduct.height = product.height
        cproduct.width = product.width
        cproduct.depth = product.depth
        cproduct.reindexObject()
        new_stock = product.stock - quantity
        product.stock = new_stock

    def add_existing_product_to_cart(self, uid, quantity):
            cproduct = self.product(uid)
            new_quantity = cproduct.quantity + quantity
            cproduct.quantity = new_quantity
            cproduct.reindexObject(idxs=['quantity'])
            original = getMultiAdapter((cproduct, self.catalog), ICartProductOriginal)
            product = IProduct(original.obj)
            new_stock = product.stock - quantity
            product.stock = new_stock

    def update_cart(self, uid, quantity):
        cproduct = self.product(uid)
        original = getMultiAdapter((cproduct, self.catalog), ICartProductOriginal)
        product = IProduct(original.obj)
        addable_quantity = product.stock + ICartProductAdapter(cproduct).quantity
        if product.unlimited_stock:
            addable_quantity = product.max_addable_quantity
            if quantity > addable_quantity:
                quantity = addable_quantity
            cproduct.quantity = quantity
            cproduct.reindexObject(idxs=['quantity'])
        else:
            if quantity <= addable_quantity:
                cproduct.quantity = quantity
                cproduct.reindexObject(idxs=['quantity'])
                new_stock = addable_quantity - quantity
#                product.stock = new_stock
            else:
                cproduct.quantity = updatable_quantity
                cproduct.reindexObject(idxs=['quantity'])
                new_stock = 0
            product.stock = new_stock

    def delete_product_from_cart(self, uid):
        cproduct = self.product(uid)
        quantity = cproduct.quantity
        original = getMultiAdapter((cproduct, self.catalog), ICartProductOriginal)
        product = IProduct(original.obj)
        new_stock = product.stock + quantity
        product.stock = new_stock
        cproduct.unindexObject()
#        path = '/'.join(cproduct.getPhysicalPath())
#        paths = [path]
#        putils = getToolByName(self.context, 'plone_utils')
#        putils.deleteObjectsByPaths(paths=paths)
#        import pdb; pdb.set_trace()
#        pass
        del self.context[cproduct.id]


class ShippingCost(object):

    adapts(ICart)
    implements(IShippingCost)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return 0


class CartItself(object):
    implements(ICartItself)
    adapts(ICart)

    def __init__(self, context):
        self.context = context

    @property
    def products(self):
        import pdb; pdb.set_trace()
        pass


    def product(self, uid):
        import pdb; pdb.set_trace()
        pass

    @property
    def subtotal(self):
        prices = [ICartProductAdapter(product).subtotal for product in self.products]
        return sum(prices)

    @property
    def shipping_cost(self):
        return 0

    @property
    def payment_cost(self):
        return 0

    @property
    def total_cost(self):
        total = self.subtotal + self.shipping_cost + self.payment_cost
        return total
