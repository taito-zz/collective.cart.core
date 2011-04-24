from zope.viewlet.interfaces import IViewletManager


class ICartConfigViewletManager(IViewletManager):
    """A viewlet manager for Cart Config."""


class IEditProductViewletManager(IViewletManager):
    """A viewlet manager for Edit Product."""


class ICartViewletManager(IViewletManager):
    """A viewlet manager for Cart."""


class ICartTotalsViewletManager(IViewletManager):
    """A viewlet manager for total prices."""


class IFixedInfoViewletManager(IViewletManager):
    """A viewlet manager for fixed infos."""
