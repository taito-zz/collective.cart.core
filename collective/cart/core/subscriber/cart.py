from zope.component import adapter
from collective.cart.core.interfaces import (
    ICart,
    IUpdateCart,
    IUpdateCartTotal,
)


@adapter(IUpdateCart)
def set_products_cost(event):
    cart = event.cart
    ICart(cart).subtotal
    item = dict(products_cost=ICart(cart).subtotal)
    cart.totals.update(item)


@adapter(IUpdateCartTotal)
def set_total_cost(event):
    cart = event.cart
    cart.total_cost = ICart(cart).total_cost
