from zope.interface import Attribute
from zope.interface import Interface


class IProduct(Interface):

    def uid():
        """Returns product uid."""

    def title():
        """Returns product title."""

    def url():
        """Returns product absolute url."""

    price = Attribute('Product Decimal Price')

    stock = Attribute('Product Stock')

    max_addable_quantity = Attribute('Product Maximum Addable Quantity')

    unlimited_stock = Attribute('Product Unlimited Stock')

    def addable_quantity():
        """Returns addable quantity."""

    def select_quantity():
        """Returns html string for <select> quantity."""

    def input_quantity():
        """Returns html string for <input> quantity."""

    def cart_folder():
        """Returns cart folder object for this product."""


class IPortalCartProperties(Interface):

    currency = Attribute('Currency')
    currency_symbol = Attribute('Currency Symbol')
    symbol_location = Attribute('Symbol Location')
    cancel_page = Attribute('Page rendered when canceled.')
    content_types = Attribute('List of Content Types which can be products.')
    decimal_type = Attribute('Decimal Type')
    cart_id_method = Attribute('Cart ID Method')
    random_cart_id_digits = Attribute('Random Cart ID Digits')
    quantity_method = Attribute('Quantity method ,select or input')

    def select_field(attribute):
        """Returns select field based on property attribute."""

    def price_with_currency(price):
        """Returns price with currency."""


class ICartProduct(Interface):

    def uid():
        """Returns original product uid."""

    def title():
        """Returns CartProduct title."""

    def quantity():
        """Returns CartProduct quantity."""

    def price():
        """Returns CartProduct price."""

    def subtotal():
        """Returns sutbotal price."""

    def product():
        """Returns original product adapted by IProduct."""

    def max_quantity():
        """Returns max quantity."""

    def select_quantity():
        """Returns html string for select quantity."""


class ICart(Interface):

    def products():
        """Returns product objects within cart."""

    def product(uid):
        """Returns a product from cart based on uid."""

    def subtotal():
        """Returns products subtotal."""

    def shipping_cost():
        """Returns shipping cost."""

    def payment_cost():
        """Returns payment cost."""

    def total_cost():
        """Returns total cost."""


class ICartFolder(Interface):

    def used_cart_ids():
        """Returns used cart ids."""

    def incremental_cart_id():
        """Incremental cart id."""

    def random_cart_id():
        """Random cart id."""

    def next_cart_id():
        """Next cart id."""

    def create_cart(session_cart_id):
        """Create cart and return it."""


class IProductAnnotationsAdapter(Interface):
    """"""


class ICartProduct(Interface):
    """"""


class IPortal(Interface):
    """Adapter interface for portal."""

    catalog = Attribute('portal_catalog')
    properties = Attribute('portal_properties')
    sdm = Attribute('session_data_manager')
    session = Attribute('Session')
    session_cart_id = Attribute('Session Cart ID')

    def cart_folder():
        """Returns cart folder."""

    def cart():
        """Returns current cart."""

    def decimal_price(price):
        """Return decimal price."""

    def add_to_cart(form):
        """Add product to cart."""

    def update_cart(form):
        """Update product in cart."""

    def delete_product(form):
        """Delete product from cart."""

    def cart_properties():
        """Cart Properties"""
