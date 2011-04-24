from zope.interface import implements
from collective.cart.core.interfaces import IUpdateCart, IUpdateCartTotal


class UpdateCart(object):

    implements(IUpdateCart)

    def __init__(self, cart):
        self.cart = cart


class UpdateCartTotal(object):

    implements(IUpdateCartTotal)

    def __init__(self, cart):
        self.cart = cart
