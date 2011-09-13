from zope.interface import Attribute
from zope.interface import Interface


class IUpdateCart(Interface):

    cart = Attribute('Cart')


class IUpdateCartTotal(Interface):

    cart = Attribute('Cart')
