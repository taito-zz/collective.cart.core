from zope.interface import implements
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.ATContentTypes.content.base import registerATCT

try:
    ## Plone4
    from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
except ImportError:
    ## Plone3
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.Archetypes.public import (
    AnnotationStorage,
    ATFieldProperty,
    Schema,
    FloatField,
    IntegerField,
    ReferenceField,
    StringField,
    DecimalWidget,
    IntegerWidget,
    SelectionWidget,
    StringWidget,
)
from collective.cart.core import CartMessageFactory as _
from collective.cart.core import PROJECTNAME
from collective.cart.core.interfaces import ICart, ICartFolder, ICartProduct

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
        default = 1,
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
        default = 5,
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
        allowed_types = ('FormFolder',),
        relationship='next_form_relationship',
    ),

),
)

finalizeATCTSchema(CartFolderSchema, folderish=True, moveDiscussion=False)

class CartFolder(ATFolder):

    implements(ICartFolder)
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

    implements(ICart)
    schema = CartSchema
    portal_type = 'Cart'

    shipping_method = None
    payment_method = None
    payer_info = None
    receiver_info = None

registerATCT(Cart, PROJECTNAME)

CartProductSchema = ATContentTypeSchema.copy() + Schema((

    StringField(
        name='uid',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
            widget=StringWidget(
                label=_(u'Original Product UID'),
            ),
        ),

    FloatField(
        name='price',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Price'),
            description=_(u''),
        ),
    ),

    IntegerField(
        name='quantity',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=IntegerWidget(
            label=_(u'Quantity'),
            description=_(u''),
        ),
    ),

    FloatField(
        name='weight',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Weight'),
        ),
    ),

    StringField(
        name='weight_unit',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=StringWidget(
            label=_(u'Weight Unit'),
        ),
    ),

    FloatField(
        name='height',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Height'),
        ),
    ),

    FloatField(
        name='width',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Width'),
        ),
    ),

    FloatField(
        name='depth',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Depth'),
        ),
    ),

),
)

finalizeATCTSchema(CartProductSchema, folderish=False, moveDiscussion=False)

class CartProduct(ATCTContent, HistoryAwareMixin):

    implements(ICartProduct)
    schema = CartProductSchema
    portal_type = 'CartProduct'

    uid = ATFieldProperty('uid')
    price = ATFieldProperty('price')
    quantity = ATFieldProperty('quantity')
    weight = ATFieldProperty('weight')
    weight_unit = ATFieldProperty('weight_unit')
    height = ATFieldProperty('height')
    width = ATFieldProperty('width')
    depth = ATFieldProperty('depth')

registerATCT(CartProduct, PROJECTNAME)
