from collective.cart.core.interfaces import IProductAnnotations
from persistent import Persistent
from zope.interface import implements


class ProductAnnotations(Persistent):

    implements(IProductAnnotations)

    def __init__(
        self,
        price=0.0,
        stock=0,
        max_addable_quantity=100,
        unlimited_stock=False,
        **kwargs
    ):
        self.price = price
        self.stock = stock
        self.max_addable_quantity = max_addable_quantity
        self.unlimited_stock = unlimited_stock
