from zope.interface import Attribute, Interface
from zope import schema
from zope.app.container.constraints import contains
from collective.cart.core import CartMessageFactory as _


#class ICartFolder(Interface):
class ICartFolderContentType(Interface):
    """Interface for CartFolder Content Type.
    """

    contains(
        'collective.cart.core.interfaces.ICartContentType',
        )

    cart_id_numbering_method = schema.Choice(
        title=_(u"Cart ID Numbering Method"),
        description=_(u"Select Incremental or Random for Cart ID Numbering."),
        required=True,
        vocabulary='Numbering Method',
        default="Incremental",
    )

    next_incremental_cart_id = schema.Int(
        title=_(u"Next Incremenatal Cart ID"),
        description=_(u"If Incrementanl Cart ID is seleceted, give interger number here."),
        required=False,
        default=1,
    )

    random_digits_cart_id = schema.Int(
        title=_(u"Random Digits Cart ID"),
        description=_(u"If Random Cart ID is selected, give integer digits here."),
        required=False,
        default=5,
    )

    quantity_method = schema.Choice(
        title=_(u"Quantity Method"),
        description=_(u"Select one method, Select or Input to determine how to put products into cart."),
        required=True,
        vocabulary="Quantity Methods",
        default="Select",
    )


#class ICart(Interface):
class ICartContentType(Interface):
    """Interface for Cart Content Type.
    """

    contains(
        'collective.cart.core.interfaces.ICartProductContentType',
        )

#    shipping_method = Attribute('Shipping Method')
#    payment_method = Attribute('Payment Method')
#    payer_info = Attribute('Customer Info')
#    receiver_info = Attribute('Receiver Info')
    info = Attribute('Additioinal Info besides products.')
    session_cart_id = Attribute('Cart ID for Session.')


#class ICartProduct(Interface):
class ICartProductContentType(Interface):
    """Interface for CartProduct content type.
    """

    uid = Attribute('Product UID')
    price = Attribute('Product Price')
    quantity = Attribute('Product Quantity')
    subtotal = Attribute('Product Subtotal')

#    uid = schema.TextLine(
#        title=_(u"Product UID"),
#        required=True,
#    )

#    price = schema.Float(
#        title=_(u"Product Price"),
#        required=True,
#    )

#    quantity = schema.Int(
#        title=_(u'Product Quantity'),
#        required=True,
#    )

#    weight = schema.Float(
#        title=_(u'Weight'),
#        required=False,
#    )

#    weight_unit=schema.TextLine(
#        title=_('Weight Unit'),
#        required=False,
#    )

#    height=schema.Float(
#        title=_(u"Height"),
#        required=False,
#    )

#    width=schema.Float(
#        title=_(u"Width"),
#        required=False,
#    )

#    depth=schema.Float(
#        title=_("Depth"),
#        required=False,
#    )
