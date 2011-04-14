from persistent import Persistent
from zope.interface import implements
from collective.cart.core.interfaces import IProductAnnotations

class ProductAnnotations(Persistent):
    implements(IProductAnnotations)
    def __init__(
        self,
        price = 0.0,
        stock = 0,
        max_addable_quantity = 100,
        unlimited_stock = False,
        weight = 0.0,
        weight_unit = 'g',
        height = 0.0,
        width = 0.0,
        depth = 0.0,
    ):
        self.price = price
        self.stock = stock
        self.max_addable_quantity = max_addable_quantity
        self.unlimited_stock = unlimited_stock
        self.weight = weight
        self.weight_unit = weight_unit
        self.height = height
        self.width = width
        self.depth = depth
