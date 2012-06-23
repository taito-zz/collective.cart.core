import mock
import unittest


class TestSalable(unittest.TestCase):

    def test_class(self):
        from collective.cart.core.behavior import Salable
        self.assertIsInstance(Salable, object)

    def create_instance(self, context=mock.Mock()):
        from collective.cart.core.behavior import Salable
        return Salable(context)

    def test_instance(self):
        instance = self.create_instance()
        from collective.cart.core.behavior import Salable
        self.assertIsInstance(instance, Salable)

    def test_instance_provides_ISalable(self):
        instance = self.create_instance()
        from collective.cart.core.interfaces import ISalable
        self.assertTrue(ISalable.providedBy(instance))

    @mock.patch('collective.cart.core.behavior.getUtility')
    def test_instance__verifyObject(self, getUtility):
        instance = self.create_instance()
        from collective.cart.core.interfaces import ISalable
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(ISalable, instance))

    def test_instance__price_empty(self):
        """First time access to price"""
        context = object()
        instance = self.create_instance(context=context)
        self.assertIsNone(instance.price)

    def test_instance__price_not_empty(self):
        """Price is not empty"""
        context = mock.Mock()
        from decimal import Decimal
        price = Decimal('5.00')
        context.price = price
        instance = self.create_instance(context=context)
        self.assertEqual(instance.price, price)

    def set_price(self, instance, price):
        """Setting price to instance."""
        instance.price = price

    def test_instance__price__ValueError(self):
        """Raise ValueError when setting other than Decimal."""
        instance = self.create_instance()
        self.assertRaises(ValueError, lambda: self.set_price(instance, 'AAA'))

    @mock.patch('collective.cart.core.behavior.getUtility')
    def test_instance__price__price(self, getUtility):
        """"""
        getUtility().forInterface().default_currency = 'EUR'
        context = mock.Mock()
        instance = self.create_instance(context=context)
        from decimal import Decimal
        price = Decimal('5.00')
        instance.price = price
        self.assertEqual(instance.context.price, price)
        from moneyed import Money
        money = Money(price, currency='EUR')
        self.assertEqual(instance.context.money, money)
        self.assertEqual(instance.money, money)

    @mock.patch('collective.cart.core.behavior.getUtility')
    def test_instance__currency(self, getUtility):
        """"""
        getUtility().forInterface().default_currency = 'EUR'
        instance = self.create_instance()
        self.assertEqual(instance.currency, 'EUR')

    def test_instance__money_empty(self):
        """First time access to price"""
        context = object()
        instance = self.create_instance(context=context)
        self.assertIsNone(instance.money)

    def set_money(self, instance, money):
        """Setting money to instance."""
        instance.money = money

    def test_instance__money__ValueError(self):
        """Raise ValueError when setting other than Money."""
        instance = self.create_instance()
        self.assertRaises(ValueError, lambda: self.set_money(instance, 'AAA'))
