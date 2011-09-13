from collective.cart.core import CartMessageFactory as _
from zope import schema
from zope.app.container.constraints import contains
from zope.interface import Attribute
from zope.interface import Interface


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


class ICartContentType(Interface):
    """Interface for Cart Content Type.
    """

    contains(
        'collective.cart.core.interfaces.ICartProductContentType',
        )

    info = Attribute('Additioinal Info besides products.')
    session_cart_id = Attribute('Cart ID for Session.')


class ICartProductContentType(Interface):
    """Interface for CartProduct content type.
    """

    uid = Attribute('Product UID')
    price = Attribute('Product Price')
    quantity = Attribute('Product Quantity')
    subtotal = Attribute('Product Subtotal')
