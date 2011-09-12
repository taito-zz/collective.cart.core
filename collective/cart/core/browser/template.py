from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.cart.core import CartMessageFactory as _
from collective.cart.core.interfaces import IPortal
from collective.cart.core.interfaces import IProduct
from collective.cart.core.interfaces import IRegularExpression
from zope.component import getMultiAdapter
from zope.component import getUtility


class CartFolderView(BrowserView):

    __call__ = ViewPageTemplateFile('templates/cart_folder.pt')


class CartTypeView(BrowserView):

    __call__ = ViewPageTemplateFile('templates/cart_type.pt')


class CartConfigView(BrowserView):

    template = ViewPageTemplateFile('templates/cart_config.pt')

    def __call__(self):
        self.request.set('disable_border', True)
        if not self.has_cart_folder:
            message = _(u"Please add CartFolder first.")
            IStatusMessage(self.request).addStatusMessage(message, type='warn')
        return self.template()

    @property
    def has_cart_folder(self):
        context = aq_inner(self.context)
        return IPortal(context).has_cart_folder


class EditProductView(BrowserView):
    template = ViewPageTemplateFile('templates/edit_product.pt')

    def __call__(self):
        form = self.request.form
        if form.get('form.button.save', None) is not None:
            context = aq_inner(self.context)
            product = IProduct(context)
            re = getUtility(IRegularExpression)
            price = form.get('price')
            if re.float(price):
                product.price = IPortal(context).decimal_price(price)
            unlimited_stock = form.get('unlimited_stock')
            if unlimited_stock == 'on':
                product.unlimited_stock = True
            if unlimited_stock != 'on':
                product.unlimited_stock = False
            stock = form.get('stock')
            if re.integer(stock):
                product.stock = int(stock)
            max_addable_quantity = form.get('max_addable_quantity')
            if re.integer(max_addable_quantity):
                product.max_addable_quantity = int(max_addable_quantity)
        return self.template()

    def fields(self):
        context = aq_inner(self.context)
        product = IProduct(context)
        res = []
        price = dict(
            label=_(u'Price'),
            description='Input Price.',
            field='<input type="text" name="price" id="price" value="%s" size="6" />' % product.price,
        )
        res.append(price)
        unlimited_stock_field = '<input type="checkbox" name="unlimited_stock" id="unlimited_stock" value="on" />'
        if product.unlimited_stock == True:
            unlimited_stock_field = '<input type="checkbox" name="unlimited_stock" id="unlimited_stock" value="on" checked="checked" />'
        unlimited_stock = dict(
            label=_(u'Unlimited Stock'),
            description=_(u'Check this if you have unlimited amount of stock.'),
            field=unlimited_stock_field,
        )
        res.append(unlimited_stock)
        stock = dict(
            label=_(u'Stock'),
            description='Input Stock.',
            field='<input type="text" name="stock" id="stock" value="%s" size="5" />' % product.stock,
        )
        res.append(stock)
        max_addable_quantity = dict(
            label=_(u'Maximum Addable Quantity'),
            description=_('You need to specify this if you checked Unlimited Stock.'),
            field='<input type="text" name="max_addable_quantity" id="max_addable_quantity" value="%s" size="5" />' % product.max_addable_quantity,
        )
        res.append(max_addable_quantity)
        return res

    @property
    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_context_state')
        return context_state.current_page_url()


class CartView(BrowserView):
    __call__ = ViewPageTemplateFile('templates/cart.pt')

    def has_contents(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('products')()
