import unittest2 as unittest


class TestCartProduct(unittest.TestCase):
    """Test CartProduct content type."""

    def createCartProduct(self):
        from Products.Archetypes.Schema.factory import instanceSchemaFactory
        from zope.component import provideAdapter
        provideAdapter(instanceSchemaFactory)
        from collective.cart.core.content.cart import CartProduct
        return CartProduct('product')

    def test_instance(self):
        from collective.cart.core.content.cart import CartProduct
        item = self.createCartProduct()
        isinstance(item, CartProduct)

    def test_portal_type(self):
        item = self.createCartProduct()
        self.assertEqual(item.portal_type, 'CartProduct')

    def test_interface(self):
        from collective.cart.core.interfaces import ICartProductContentType
        item = self.createCartProduct()
        self.assertTrue(ICartProductContentType.providedBy(item))

    def test_schema_fields(self):
        item = self.createCartProduct()
        names = [
            'id',
            'title',
            'description',
        ]
        self.assertEqual(
            [field.getName() for field in item.schema.getSchemataFields('default')],
            names
        )

    def test_variables(self):
        item = self.createCartProduct()
        self.failIf(item.uid)
        self.failIf(item.price)
        self.failIf(item.quantity)
        self.failIf(item.subtotal)
