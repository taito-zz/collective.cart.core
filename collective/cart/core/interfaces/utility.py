from zope.interface import Interface


class IPriceInString(Interface):

    def __call__(price, currency="EUR", point='.'):
        """Returns price in string based on its currency and point type."""


class IPriceWithCurrency(Interface):

    def __call__(price, currency, position, point, symbol):
        """Returns price with currency."""


class IPrice(Interface):

    def __call__(price):
        """Retruns price in decimal, string or float"""


class IDecimalPlaces(Interface):

    def __call__(currency):
        """Returns decimal places against currency."""


class ISelectRange(Interface):

    def __call__(number):
        """Returns list of series of numbers from one."""


class IRandomDigits(Interface):

    def __call__(number, ids):
        """Returns randome digits which is not in ids."""


class IRegularExpression(Interface):

    def email(string):
        """Returns True if string is e-mail address if else False."""

    def integer(string):
        """Returns True if string can be integer if else False."""

    def float(string):
        """Returns True if string can be float if else False."""
