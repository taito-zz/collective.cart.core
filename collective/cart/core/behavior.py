from collective.cart.core import _
# from decimal import ROUND_HALF_UP
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.schema import Decimal as sDecimal
from zope.schema import TextLine
from zope.schema.interfaces import IDecimal
from zope.schema.interfaces import IFromUnicode
from rwproperty import getproperty
from rwproperty import setproperty
from zope.schema import ValidationError
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from moneyed import Money
from decimal import Decimal
from collective.cart.core.registry import ICurrency
from moneyed.localization import format_money
from zope.component import getMultiAdapter
from zope.interface import Attribute
from collective.cart.core.interfaces import ISalable

import logging

logger = logging.getLogger(__name__)


alsoProvides(ISalable, form.IFormFieldProvider)


class Salable(object):
    """
    """
    implements(ISalable)

    def __init__(self, context):
        self.context = context

    @getproperty
    def price(self):
        return getattr(self.context, 'price', None)

    @setproperty
    def price(self, value):
        """Setting price as Decimal and money as Money.

        :param value: Price value such as 5.00, 5,00 nor 1800.
        :type value: str
        """
        if isinstance(value, Decimal):
            # Set price
            setattr(self.context, 'price', value)
            # Set money
            setattr(self.context, 'money', Money(value, currency=self.currency))
        else:
            raise ValueError('Not Decimal.')

    @property
    def currency(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(ICurrency).default_currency

    @getproperty
    def money(self):
        return getattr(self.context, 'money', None)

    @setproperty
    def money(self, value):
        """Setting money as Money.

        :param value: Money instance.
        :type value: moneyed.Money
        """
        if isinstance(value, Money):
            setattr(self.context, 'money', value)
        else:
            raise ValueError('Not Money.')


