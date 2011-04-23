from zope.viewlet.interfaces import IViewletManager

class ICartConfigViewletManager(IViewletManager):
    """A viewlet manager for Cart Config."""

class ICartViewletManager(IViewletManager):
    """A viewlet manager for Cart."""

class ICartTotalsViewletManager(IViewletManager):
    """A viewlet manager for total prices."""

class IFixedInfoViewletManager(IViewletManager):
    """A viewlet manager for fixed infos."""
