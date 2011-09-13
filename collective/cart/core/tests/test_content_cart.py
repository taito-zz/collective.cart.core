import unittest2 as unittest


class TestCart(unittest.TestCase):
    """Test Cart content type."""

    def createCart(self):
        from Products.Archetypes.Schema.factory import instanceSchemaFactory
        from zope.component import provideAdapter
        provideAdapter(instanceSchemaFactory)
        from collective.cart.core.content.cart import Cart
        return Cart('cart')

    def test_instance(self):
        from collective.cart.core.content.cart import Cart
        item = self.createCart()
        isinstance(item, Cart)

    def test_portal_type(self):
        item = self.createCart()
        self.assertEqual(item.portal_type, 'Cart')

    def test_interface(self):
        from collective.cart.core.interfaces import ICartContentType
        item = self.createCart()
        self.assertTrue(ICartContentType.providedBy(item))

    def test_schema_fields(self):
        item = self.createCart()
        names = [
            'id',
            'title',
            'description',
            'constrainTypesMode',
            'locallyAllowedTypes',
            'immediatelyAddableTypes',
        ]
        self.assertEqual(
            [field.getName() for field in item.schema.getSchemataFields('default')],
            names
        )

    def test_variables(self):
        from persistent.dict import PersistentDict
        item = self.createCart()
        isinstance(item.info, PersistentDict)
        self.failIf(item.session_cart_id)
        isinstance(item.totals, PersistentDict)
        self.failIf(item.total_cost)
