from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.public import ATFieldProperty
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from collective.cart.core import CartMessageFactory as _
from collective.cart.core import PROJECTNAME
from collective.cart.core.interfaces import ICartContentType
from collective.cart.core.interfaces import ICartFolderContentType
from collective.cart.core.interfaces import ICartProductContentType
from persistent.dict import PersistentDict
from zope.interface import implements


CartFolderSchema = ATFolderSchema.copy() + Schema((

    StringField(
        name='cart_id_numbering_method',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=SelectionWidget(
            label=_(u'Cart ID Numbering Method'),
            description=_(u'Select Incremental or Random for Cart ID Numbering.'),
        ),
        vocabulary=('Incremental', 'Random'),
        enforceVocabulary=True,
        default='Incremental',
    ),

    IntegerField(
        name='next_incremental_cart_id',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=IntegerWidget(
            label=_(u'Next Incremental Cart ID'),
            description=_(u'If Incrementanl Cart ID is seleceted, give interger number here.'),
        ),
        default=1,
    ),

    IntegerField(
        name='random_digits_cart_id',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=IntegerWidget(
            label=_(u'Random Digits Cart ID'),
            description=_(u'If Random Cart ID is selected, give integer digits here.'),
        ),
        default=5,
    ),

    StringField(
        name='quantity_method',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=SelectionWidget(
            label=_(u'Quantity Method'),
            description=_(u'Select one method, Select or Input to determine how to put products into cart.'),
        ),
        vocabulary=('Select', 'Input'),
        enforceVocabulary=True,
        default='Select',
    ),

    ReferenceField(
        name='next_form',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            show_indexes=True,
            force_close_on_insert=True,
            label=_(u'Next Form'),
            description=_(u'Select next form for check out. Only FormFolder from PloneFormGen is available.'),
        ),
        allowed_types=('FormFolder',),
        relationship='next_form_relationship',
    ),

),
)

finalizeATCTSchema(CartFolderSchema, folderish=True, moveDiscussion=False)


class CartFolder(ATFolder):

    implements(ICartFolderContentType)
    schema = CartFolderSchema
    portal_type = 'CartFolder'

    cart_id_numbering_method = ATFieldProperty('cart_id_numbering_method')
    next_incremental_cart_id = ATFieldProperty('next_incremental_cart_id')
    random_digits_cart_id = ATFieldProperty('random_digits_cart_id')
    quantity_method = ATFieldProperty('quantity_method')
    next_form = ATFieldProperty('next_form')

registerATCT(CartFolder, PROJECTNAME)

CartSchema = ATFolderSchema.copy()

finalizeATCTSchema(CartSchema, folderish=True, moveDiscussion=False)


class Cart(ATFolder):

    implements(ICartContentType)
    schema = CartSchema
    portal_type = 'Cart'

    info = PersistentDict()
    session_cart_id = None
    totals = PersistentDict()
    total_cost = None

registerATCT(Cart, PROJECTNAME)

# CartProductSchema = ATContentTypeSchema.copy() + Schema((

#     StringField(
#         name='uid',
#         required=True,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#             widget=StringWidget(
#                 label=_(u'Original Product UID'),
#             ),
#         ),

#     FloatField(
#         name='price',
#         required=True,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=DecimalWidget(
#             label=_(u'Price'),
#             description=_(u''),
#         ),
#     ),

#     IntegerField(
#         name='quantity',
#         required=True,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=IntegerWidget(
#             label=_(u'Quantity'),
#             description=_(u''),
#         ),
#     ),

#     FloatField(
#         name='weight',
#         required=False,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=DecimalWidget(
#             label=_(u'Weight'),
#         ),
#     ),

#     StringField(
#         name='weight_unit',
#         required=False,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=StringWidget(
#             label=_(u'Weight Unit'),
#         ),
#     ),

#     FloatField(
#         name='height',
#         required=False,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=DecimalWidget(
#             label=_(u'Height'),
#         ),
#     ),

#     FloatField(
#         name='width',
#         required=False,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=DecimalWidget(
#             label=_(u'Width'),
#         ),
#     ),

#     FloatField(
#         name='depth',
#         required=False,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=DecimalWidget(
#             label=_(u'Depth'),
#         ),
#     ),

#     FloatField(
#         name='depth',
#         required=False,
#         searchable=False,
#         languageIndependent=True,
#         storage=AnnotationStorage(),
#         widget=DecimalWidget(
#             label=_(u'Dimension'),
#         ),
#     ),

# ),
# )

# finalizeATCTSchema(CartProductSchema, folderish=False, moveDiscussion=False)


#class CartProduct(ATCTContent, HistoryAwareMixin):
class CartProduct(ATCTContent):

#    implements(ICartProduct)
    implements(ICartProductContentType)
#    schema = CartProductSchema
    portal_type = 'CartProduct'

#    uid = ATFieldProperty('uid')
#    price = ATFieldProperty('price')
#    quantity = ATFieldProperty('quantity')
    uid = None
    price = None
    quantity = None
    subtotal = None
#    weight = ATFieldProperty('weight')
#    weight_unit = ATFieldProperty('weight_unit')
##    height = ATFieldProperty('height')
##    width = ATFieldProperty('width')
##    depth = ATFieldProperty('depth')
#    dimension = ATFieldProperty('dimension')

registerATCT(CartProduct, PROJECTNAME)
