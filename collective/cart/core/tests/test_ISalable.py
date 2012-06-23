import unittest


class TestISalable(unittest.TestCase):

    def test_subclass(self):
        from plone.directives.form import Schema
        from collective.cart.core.behavior import ISalable
        self.assertTrue(issubclass(ISalable, Schema))

    def get_schema(self, name):
        """Get schema of ISalable interface.

        :param name: Name of schema.
        :type name: str
        """
        from collective.cart.core.behavior import ISalable
        return ISalable.get(name)

    def test_price__instance(self):
        from zope.schema import Decimal
        schema = self.get_schema('price')
        self.assertTrue(isinstance(schema, Decimal))

    def test_price__title(self):
        schema = self.get_schema('price')
        self.assertEqual(schema.title, u'Price')

    def test_price__required(self):
        schema = self.get_schema('price')
        self.assertTrue(schema.required)

    def test_money__instance(self):
        from zope.interface import Attribute
        schema = self.get_schema('money')
        self.assertTrue(isinstance(schema, Attribute))

    def test_money__doc(self):
        from zope.interface import Attribute
        schema = self.get_schema('money')
        self.assertEqual(schema.getDoc(), 'Money instance')
