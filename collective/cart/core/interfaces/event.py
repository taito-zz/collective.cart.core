from zope.interface import Attribute, Interface


class IUpdateCart(Interface):

    cart = Attribute('Cart')


class IUpdateCartTotal(Interface):

    cart = Attribute('Cart')
