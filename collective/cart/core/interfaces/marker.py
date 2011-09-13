from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import Interface


class IPotentiallyAddableToCart(Interface):
    """Marker interface to content type instance to make potentially addable to cart."""


class IAddableToCart(IPotentiallyAddableToCart, IAttributeAnnotatable):
    """Marker interface to content type instance which is made addable to cart."""


class IProductAnnotations(Interface):
    """Marker interface for product information stored in annotation."""


class ICartAware(Interface):
    """Marker interface for content types to make cart aware."""
