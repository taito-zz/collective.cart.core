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


class ISalable(form.Schema):
    """Add salable field to dexterity type.
    """

    price = sDecimal(
    # price = TextLine(
            title=_(u"Price"),
            # description=_(u"Price"),
            required=True,
            # allow_uncommon=True,
        )

    money = Attribute('Money instance')
