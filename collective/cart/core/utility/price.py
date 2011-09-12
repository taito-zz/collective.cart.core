from collective.cart.core.config import CURRENCY_DECIMAL
from collective.cart.core.interfaces import IDecimalPlaces
from collective.cart.core.interfaces import IPrice
from collective.cart.core.interfaces import IPriceInString
from collective.cart.core.interfaces import IPriceWithCurrency
from decimal import Decimal
from decimal import ROUND_HALF_UP
from zope.component import getUtility
from zope.interface import implements


class Price(object):

    implements(IPrice)

    def __init__(self, type_in_string):
        self.type = type_in_string

    def __call__(self, price, decimal=2):
        if decimal == 3:
            price = Decimal(str(price)).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
            price = Decimal(price).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
            if self.type == "decimal":
                return price
            if self.type == "string":
                return str(price)
            if self.type == "float":
                return float(price)
        if decimal == 2:
            price = Decimal(str(price)).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
            price = Decimal(price).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            if self.type == "decimal":
                return price
            if self.type == "string":
                return str(price)
            if self.type == "float":
                return float(price)
        else:
            price = Decimal(str(price)).quantize(Decimal('.1'), rounding=ROUND_HALF_UP)
            price = Decimal(price).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
            if self.type == "decimal":
                return price
            if self.type == "string":
                return str(price)
            if self.type == "float":
                return float(price)

float_price = Price("float")
decimal_price = Price("decimal")
string_price = Price("string")


class PriceInString(object):

    implements(IPriceInString)

    def __call__(self, price, currency="EUR", point='.'):
        """Returns price in string."""
        places = getUtility(IDecimalPlaces)(currency)
        price = getUtility(IPrice, name="string")(price, places)
        if point == ',':
            price = price.replace('.', ',')
        return price


class PriceWithCurrency(object):

    implements(IPriceWithCurrency)

    def __call__(self, price, currency='EUR', position='front', point='.', symbol=None):
        """Returns price with currency."""
        places = getUtility(IDecimalPlaces)(currency)
        price = getUtility(IPrice, name="string")(price, places)
        if point == ',':
            price = price.replace('.', ',')
        symbol = symbol or currency
        if position == 'front':
            return '%s %s' % (symbol, price)
        else:
            return '%s %s' % (price, symbol)


class DecimalPlaces(object):
    implements(IDecimalPlaces)

    def __call__(self, currency):
        places = CURRENCY_DECIMAL.get(currency)
        if places is not None:
            return CURRENCY_DECIMAL.get(currency)
        else:
            return 2
