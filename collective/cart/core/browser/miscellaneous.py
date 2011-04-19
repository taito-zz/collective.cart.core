#try:
#    import hashlib
#except ImportError:
#    import md5
from Acquisition import aq_inner, aq_parent
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter, getUtility
from zope.interface import alsoProvides, noLongerProvides
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import (
    IAddableToCart,
    ICartAdapter,
    ICartAware,
    ICartItself,
    ICartProductAdapter,
    IPortalCartProperties,
    IPortalCatalog,
    IPortalSessionCatalog,
    IPotentiallyAddableToCart,
#    IPrice,
    IPriceInString,
    ICartProductOriginal,
)

class Miscellaneous(BrowserView):

    def potentially_addable_but_not_addable_to_cart(self):
        context = aq_inner(self.context)
        return IPotentiallyAddableToCart.providedBy(context) and not IAddableToCart.providedBy(context)

    def addable_to_cart(self):
        context = aq_inner(self.context)
        return IPotentiallyAddableToCart.providedBy(context) and IAddableToCart.providedBy(context)

    def make_addable_to_cart(self):
        context = aq_inner(self.context)
        if IPotentiallyAddableToCart.providedBy(context):
            alsoProvides(context, IAddableToCart)
            url = '%s/@@edit-product' %context.absolute_url()
            IAnnotations(context)['collective.cart.core'] = ProductAnnotations()
            return self.request.response.redirect(url)

    def make_not_addable_to_cart(self):
        context = aq_inner(self.context)
        noLongerProvides(context, IAddableToCart)
        url = context.absolute_url()
        del IAnnotations(context)['collective.cart.core']
        return self.request.response.redirect(url)

    def has_cart_contents(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sdm = getToolByName(portal, 'session_data_manager')
        catalog = getToolByName(portal, 'portal_catalog')
        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
        if cart is not None:
            return getMultiAdapter((cart, catalog), ICartAdapter).products

    def products(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        catalog = getToolByName(portal, 'portal_catalog')
        sdm = getToolByName(portal, 'session_data_manager')
        properties = getToolByName(portal, 'portal_properties')
        pcp = IPortalCartProperties(properties)
        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
        products = getMultiAdapter((cart, catalog), ICartAdapter).products
        if products is not None:
            res = []
            for product in products:
                cpo = getMultiAdapter((product, catalog), ICartProductOriginal)
                cpa = ICartProductAdapter(product)
                item = dict(
                    title = cpa.title,
                    quantity = cpa.quantity,
                    uid = cpa.uid,
                    url = cpo.url,
                    select_quantity = cpo.select_quantity,
                    price_with_currency = pcp.price_with_currency(cpa.price),
                    subtotal_with_currency = pcp.price_with_currency(cpa.subtotal),
                )
                res.append(item)
            return res

    def totals_with_currency(self):
#        if self.products() is not None:
        if self.has_cart_contents():
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            portal = portal_state.portal()
            catalog = getToolByName(portal, 'portal_catalog')
            sdm = getToolByName(portal, 'session_data_manager')
            properties = getToolByName(portal, 'portal_properties')
            pcp = IPortalCartProperties(properties)
            cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
            ca = getMultiAdapter((cart, catalog), ICartAdapter)
            ci = ICartItself(cart)
            shipping_cost_with_currency = pcp.price_with_currency(ci.shipping_cost)
            if ci.shipping_cost == 0:
                shipping_cost_with_currency = None
            payment_cost_with_currency = pcp.price_with_currency(ca.payment_cost)
            if ca.payment_cost == 0:
                payment_cost_with_currency = None
            data = dict(
                products_subtotal_with_currency = pcp.price_with_currency(ca.subtotal),
                shipping_cost_with_currency = shipping_cost_with_currency,
                payment_cost_with_currency = payment_cost_with_currency,
                total_cost_with_currency = pcp.price_with_currency(ca.total_cost),
            )
            return data


    def cart_id(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sdm = getToolByName(portal, 'session_data_manager')
        catalog = getToolByName(portal, 'portal_catalog')
        return getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart_id

    def total_price(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sdm = getToolByName(portal, 'session_data_manager')
        catalog = getToolByName(portal, 'portal_catalog')
        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
        if cart is not None:
            price = getMultiAdapter((cart, catalog), ICartAdapter).total_cost
            pis = getUtility(IPriceInString)
            return pis(price)

    def next_step(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        catalog = getToolByName(portal, 'portal_catalog')
        cfolder = getMultiAdapter((portal, catalog), IPortalCatalog).cart_folder
        form = cfolder.getNext_form()
        if form is not None:
            self.request.response.redirect(form.absolute_url())
        else:
            context.restrictedTraverse('test-step')

    def test_step(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        catalog = getToolByName(portal, 'portal_catalog')

#    def verkkomaksut_on_success(self, fields, REQUEST):
#        context = aq_inner(self.context) 
#        portal = getToolByName(context, 'portal_url').getPortalObject()
#        sdm = getToolByName(context, 'session_data_manager')
#        catalog = getToolByName(context, 'portal_catalog')
#        psc = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog)
#        if psc.cart is not None:
#            order_number = psc.cart_id
#            ORDER_NUMBER = order_number
#            field = context.selected_price_field()
#            form = context.REQUEST.form
#            price = form.get(field)
#            ca = getMultiAdapter((psc.cart, catalog), ICartAdapter)
#            string_price = getUtility(IPrice, name="string")
#            price = string_price(ca.total_cost)
#            MERCHANT_ID = str(context.getMerchant_id())
#            AMOUNT = price
#            ORDER_DESCRIPTION = context.order_description(fields, REQUEST)
#            CURRENCY = 'EUR'
#            parent = aq_parent(aq_inner(context))
#            parent_url = parent.absolute_url()
#            return_url = '%s/@@verkkomaksut-success' % (parent_url)
#            cancel_url = '%s/@@verkkomaksut-canceled' %(context.absolute_url())
#            notify_url = '%s/@@verkkomaksut-notify' % (context.absolute_url())
#            RETURN_ADDRESS = return_url
#            CANCEL_ADDRESS = cancel_url
#            NOTIFY_ADDRESS = notify_url
#            TYPE = 'S1'
#            CULTURE = 'fi_FI'
#            MODE = '1'
#            ADAPTER_UID = context.UID()

##            sdm = getToolByName(context, 'session_data_manager')
#            session = sdm.getSessionData(create=True)
#            try:
#                m = hashlib.md5()
#            except:
#                m = md5.new()
#            m.update(context.getMerchant_authentication_code())
#            ## For TYPE S1
#            m.update('|' + MERCHANT_ID)
#            m.update('|' + AMOUNT)
#            m.update('|' + ORDER_NUMBER)
#            m.update('||' + ORDER_DESCRIPTION)
#            m.update('|' + CURRENCY)
#            m.update('|' + RETURN_ADDRESS)
#            m.update('|' + CANCEL_ADDRESS)
#            m.update('||' + NOTIFY_ADDRESS)
#            m.update('|' + TYPE)
#            m.update('|' + CULTURE)
#            m.update('||' + MODE + '||')
#            auth_code = m.hexdigest()
#            AUTHCODE = auth_code.upper()

#            value = dict(
#                MERCHANT_ID = MERCHANT_ID,
#                AMOUNT = AMOUNT,
#                ORDER_NUMBER = ORDER_NUMBER,
#                ORDER_DESCRIPTION = ORDER_DESCRIPTION,
#                CURRENCY = CURRENCY,
#                RETURN_ADDRESS = RETURN_ADDRESS,
#                CANCEL_ADDRESS = CANCEL_ADDRESS,
#                NOTIFY_ADDRESS = NOTIFY_ADDRESS,
#                TYPE = TYPE,
#                CULTURE = CULTURE,
#                MODE = MODE,
#                AUTHCODE = AUTHCODE,
#                ADAPTER_UID = ADAPTER_UID,
#            )

#            session.set('pfg.verkkomaksut', value)
#            session.set('pfg.verkkomaksut.fields', context.displayInputs(REQUEST))


#            url = '%s/@@verkkomaksut' % parent_url
#        else:
#            url = '%s/@@cart' % portal.absolute_url()
#        return context.REQUEST.RESPONSE.redirect(url)

    def make_cart_aware(self):
        context = aq_inner(self.context)
        alsoProvides(context, ICartAware)
        parent = aq_parent(context)
        alsoProvides(parent, ICartAware)
        url = context.absolute_url()
        return self.request.response.redirect(url)

    def make_not_cart_aware(self):
        context = aq_inner(self.context)
        noLongerProvides(context, ICartAware)
        parent = aq_parent(context)
        noLongerProvides(parent, ICartAware)
        url = context.absolute_url()
        return self.request.response.redirect(url)

    def is_cart_aware(self):
        context = aq_inner(self.context)
        return ICartAware.providedBy(context)

