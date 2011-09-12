from Acquisition import aq_parent
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts, getUtility
from zope.interface import implements
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IAddableToCart
from collective.cart.core.interfaces import ICartFolderContentType
from collective.cart.core.interfaces import IPortal
from collective.cart.core.interfaces import IProduct
from collective.cart.core.interfaces import ISelectRange


class Product(object):

    adapts(IAddableToCart)
    implements(IProduct)

    def __init__(self, context):
        self.context = context

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        else:
            annotations = IAnnotations(self.context)
            if annotations.get('collective.cart.core', None) is None:
                annotations['collective.cart.core'] = ProductAnnotations()
            return getattr(annotations['collective.cart.core'], attr)

    def __setattr__(self, attr, value):
        if attr == 'context':
            self.__dict__[attr] = value
        else:
            annotations = IAnnotations(self.context)
            setattr(annotations['collective.cart.core'], attr, value)

    @property
    def uid(self):
        return self.context.UID()

    @property
    def title(self):
        return self.context.Title()

    @property
    def url(self):
        return self.context.absolute_url()

    @property
    def addable_quantity(self):
        if self.unlimited_stock:
            return self.max_addable_quantity
        else:
            if self.max_addable_quantity > self.stock:
                return self.stock
            else:
                return self.max_addable_quantity

    @property
    def select_quantity(self):
        if self.addable_quantity > 0:
            html = '<select id="quantity" name="quantity">'
            for qtt in getUtility(ISelectRange)(self.addable_quantity):
                html += '<option value="%s">%s</option>' % (qtt,  qtt)
            html += '</select>'
            return html

    @property
    def input_quantity(self):
        if self.addable_quantity > 0:
            html = '<input type="text "id="quantity" name="quantity" size="3" value="" />'
            return html

    @property
    def html_quantity(self):
        context = aq_inner(self.context)
        if IPortal(context).cart_folder.quantity_method == 'Select':
            return self.select_quantity
        else:
            return self.input_quantity

    @property
    def cart_folder(self):
        context = aq_inner(self.context)
        while not [obj for obj in aq_parent(context).objectValues() if ICartFolderContentType.providedBy(obj)]:
            context = aq_parent(context)
        return [obj for obj in aq_parent(context).objectValues() if ICartFolderContentType.providedBy(obj)][0]
