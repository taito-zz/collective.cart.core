from zope.interface import Interface, Attribute

class IProduct(Interface):

    def uid():
        """Returns product uid."""

    def title():
        """Returns product title."""

    price = Attribute('Product Price')

    stock = Attribute('Product Stock')

    max_addable_quantity = Attribute('Product Maximum Addable Quantity')

    unlimited_stock = Attribute('Product Unlimited Stock')

    weight = Attribute('Product Weight')

    weight_unit = Attribute('Product Weight Unit')

    height = Attribute('Product Height')

    width = Attribute('Product Width')

    depth = Attribute('Product Depth')

    def dimension(self, height, width, depth):
        """Product dimention"""

    def weight_in_kg(ratio):
        """Returns weight in kg."""

    def addable_quantity():
        """Returns addable quantity."""

    def select_quantity():
        """Returns html string for <select> quantity."""

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


class ICartProductAdapter(Interface):

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


class ICartProductOriginal(Interface):

    def brain():
        """Returns original product brain."""

    def obj():
        """Retruns original product object."""

    def url():
        """Returns original product url."""

    def updateble_quantity():
        """Returns updatable quantity."""

    def select_quantity():
        """Returns select html string."""

class ICartAdapter(Interface):

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
