from collective.cart.core import _
from plone.directives import form
from zope.schema import Decimal
from zope.interface import Attribute


class ISalable(form.Schema):
    """Add salable field to dexterity type.
    """

    price = Decimal(
            title=_(u"Price"),
            required=True,
    )

    currency = Attribute('Currency like EUR')
    money = Attribute('Money instance')
