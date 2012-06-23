from zope.interface import Interface
from zope.schema import Choice
from collective.cart.core import _

from moneyed.classes import CURRENCIES


currencies = CURRENCIES.keys()
currencies.sort()


class ICurrency(Interface):

    default_currency = Choice(
        title=_(u'Default Currency'),
        description=_(u'Default Currency for price field.'),
        required=True,
        values=currencies,
        default='EUR',
    )
