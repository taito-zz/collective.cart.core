import unittest2 as unittest


class TestCartFolder(unittest.TestCase):
    """Test CartFolder content type."""

    def createCartFolder(self):
        from Products.Archetypes.Schema.factory import instanceSchemaFactory
        from zope.component import provideAdapter
        provideAdapter(instanceSchemaFactory)
        from collective.cart.core.content.cart import CartFolder
        return CartFolder('cfolder')

    def test_instance(self):
        from collective.cart.core.content.cart import CartFolder
        item = self.createCartFolder()
        isinstance(item, CartFolder)

    def test_portal_type(self):
        item = self.createCartFolder()
        self.assertEqual(item.portal_type, 'CartFolder')

    def test_interface(self):
        from collective.cart.core.interfaces import ICartFolderContentType
        item = self.createCartFolder()
        self.assertTrue(ICartFolderContentType.providedBy(item))

    def test_schema_fields(self):
        item = self.createCartFolder()
        names = [
            'id',
            'title',
            'description',
            'constrainTypesMode',
            'locallyAllowedTypes',
            'immediatelyAddableTypes',
            'cart_id_numbering_method',
            'next_incremental_cart_id',
            'random_digits_cart_id',
            'quantity_method',
            'next_form'
        ]
        self.assertEqual(
            [field.getName() for field in item.schema.getSchemataFields('default')],
            names
        )

    def test_field__cart_id_numbering_method(self):
        item = self.createCartFolder()
        field = item.schema['cart_id_numbering_method']
        from Products.Archetypes.Field import StringField
        isinstance(field, StringField)
        self.assertTrue(field.required)
        self.assertFalse(field.searchable)
        self.assertTrue(field.languageIndependent)
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from Products.Archetypes.public import SelectionWidget
        isinstance(widget, SelectionWidget)
        self.assertEqual(widget.label, u'Cart ID Numbering Method')
        self.assertEqual(
            widget.description,
            u'Select Incremental or Random for Cart ID Numbering.'
        )
        self.assertEqual(field.default, u'Incremental')
        self.assertEqual(field.vocabulary, (u'Incremental', u'Random'))
        self.assertTrue(field.enforceVocabulary)
        item.cart_id_numbering_method = u'Random'
        self.assertEqual(item.getCart_id_numbering_method(), u'Random')

    def test_field__next_incremental_cart_id(self):
        item = self.createCartFolder()
        field = item.schema['next_incremental_cart_id']
        from Products.Archetypes.Field import IntegerField
        isinstance(field, IntegerField)
        self.assertFalse(field.required)
        self.assertFalse(field.searchable)
        self.assertTrue(field.languageIndependent)
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from Products.Archetypes.public import IntegerWidget
        isinstance(widget, IntegerWidget)
        self.assertEqual(widget.label, u'Next Incremental Cart ID')
        self.assertEqual(
            widget.description,
            u'If Incrementanl Cart ID is seleceted, give interger number here.'
        )
        self.assertEqual(field.default, 1)
        item.next_incremental_cart_id = 3
        self.assertEqual(item.getNext_incremental_cart_id(), 3)

    def test_field__random_digits_cart_id(self):
        item = self.createCartFolder()
        field = item.schema['random_digits_cart_id']
        from Products.Archetypes.Field import IntegerField
        isinstance(field, IntegerField)
        self.assertFalse(field.required)
        self.assertFalse(field.searchable)
        self.assertTrue(field.languageIndependent)
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from Products.Archetypes.public import IntegerWidget
        isinstance(widget, IntegerWidget)
        self.assertEqual(widget.label, u'Random Digits Cart ID')
        self.assertEqual(
            widget.description,
            u'If Random Cart ID is selected, give integer digits here.'
        )
        self.assertEqual(field.default, 5)
        item.random_digits_cart_id = 3
        self.assertEqual(item.getRandom_digits_cart_id(), 3)

    def test_field__quantity_method(self):
        item = self.createCartFolder()
        field = item.schema['quantity_method']
        from Products.Archetypes.Field import StringField
        isinstance(field, StringField)
        self.assertTrue(field.required)
        self.assertFalse(field.searchable)
        self.assertTrue(field.languageIndependent)
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from Products.Archetypes.public import SelectionWidget
        isinstance(widget, SelectionWidget)
        self.assertEqual(widget.label, u'Quantity Method')
        self.assertEqual(
            widget.description,
            u'Select one method, Select or Input to determine how to put products into cart.'
        )
        self.assertEqual(field.default, u'Select')
        self.assertEqual(field.vocabulary, (u'Select', u'Input'))
        self.assertTrue(field.enforceVocabulary)
        item.quantity_method = u'Input'
        self.assertEqual(item.getQuantity_method(), u'Input')

    def test_field__next_form(self):
        item = self.createCartFolder()
        field = item.schema['next_form']
        from Products.Archetypes.Field import ReferenceField
        isinstance(field, ReferenceField)
        self.assertFalse(field.required)
        self.assertFalse(field.searchable)
        self.assertTrue(field.languageIndependent)
        from Products.Archetypes.public import AnnotationStorage
        isinstance(field.storage, AnnotationStorage)
        widget = field.widget
        from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
        isinstance(widget, ReferenceBrowserWidget)
        self.assertEqual(widget.label, u'Next Form')
        self.assertEqual(
            widget.description,
            u'Select next form for check out. Only FormFolder from PloneFormGen is available.'
        )
        self.assertEqual(field.allowed_types, ('FormFolder',))
        self.assertEqual(field.relationship, 'next_form_relationship')
