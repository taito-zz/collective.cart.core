from collective.cart.core import _
from decimal import ROUND_HALF_UP
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.schema import Decimal
from zope.schema.interfaces import IDecimal
from zope.schema.interfaces import IFromUnicode



# class IPrice(IDecimal):
#     u"""Field containing a Price."""


# class Price(Decimal):
#     __doc__ = IPrice.__doc__
#     implements(IPrice, IFromUnicode)
#     """
#     """

#     def __init__(self, *args, **kw):
#         super(Decimal, self).__init__(*args, **kw)


class ISalable(form.Schema):
    """Add salable field to dexterity type.
    """

    price = Decimal(
            title=_(u"Price"),
            # description=_(u"Price"),
            required=True,
            # allow_uncommon=True,
        )


alsoProvides(ISalable, form.IFormFieldProvider)


class Salable(object):
    """
    """
    implements(ISalable)

    def __init__(self, context):
        self.context = context

    # @getproperty
    # def tags(self):
    #     return set(self.context.Subject())
    # @setproperty
    # def tags(self, value):
    #     if value is None:
    #         value = ()
    #     self.context.setSubject(tuple(value))