from zope.interface import Interface, Attribute

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

class IPortalSession(Interface):

    cart_id = Attribute('Cart ID')

    def delete_cart_id_from_session():
        """Delete current cart id from session."""

class IPortalSessionCatalog(Interface):

    cart_id = Attribute('Cart ID')

    def cart():
        """Returns current cart object from session."""

    def add_to_cart(uid, quantity, cart_id):
        """Add to cart."""

    def add_to_cart_first_time(uid, quantity):
        """Add product to cart first time."""

    

class IPortalCatalog(Interface):

#    def cart_folder():
#        """Returns Cart Folder."""

    def used_cart_ids():
        """Returns list of already used cart ids."""

    def incremental_cart_id():
        """Rerturns new incremental cart id and set the next cart id added by one."""

    def random_cart_id(digits):
        """Returns new random cart id."""

class IPortalAdapter(Interface):

    def cart_properties():
        """Returns portal IPortalCartProperties adapted."""

    def next_cart_id(method, digits):
        """Returns next cart id based on the method and digits."""

class IPortalCart(Interface):

    def add_to_cart():
        """Method to add product to cart."""

    def update_cart():
        """Update cart."""

    def delete_product_from_cart():
        """Delete product from cart."""


class IShippingCost(Interface):

    def __call__():
        """Returns shipping cost."""


class IAvailableShippingMethods(Interface):

    def __call__():
        """Returns available shipping methods."""

class IUpdateShippingMethod(Interface):

    def __call__(method):
        """Update shipping method."""

class IProductAnnotationsAdapter(Interface):
    """"""

class ICartItself(Interface):

    def products():
        """Returns all the products under the cart."""

    def product(uid):
        """Returns product with uid."""

    def subtotal():
        """Returns products subtotal."""

    def weight():
        """Returns products total weight."""

    def shipping_cost():
        """"""

class ICartProduct(Interface):
    """"""

#class IContext(Interface):

#    def get_closest_content(interface):
#        """Get closest content from child."""

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

