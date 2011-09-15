from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from collective.cart.core.tests.base import IntegrationTestCase


class TestSetup(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.site_properties = getattr(self.properties, 'site_properties')
        self.navtree_properties = getattr(self.properties, 'navtree_properties')
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.content_types = [
            'Cart',
            'CartFolder',
            'CartProduct',
        ]
        self.types = getToolByName(self.portal, 'portal_types')
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.actions = getToolByName(self.portal, 'portal_actions')
        self.sm = getSecurityManager()

    def test_is_collective_cart_installed(self):
        self.failUnless(self.installer.isProductInstalled('collective.cart.core'))

    ## Content Types
    def test_content_installed(self):
        for type in self.content_types:
            self.failUnless(type in self.types.objectIds())

    def test_CartFolder_content_type(self):
        item = self.types.getTypeInfo('CartFolder')
        self.assertEquals('CartFolder', item.title)
        self.assertEquals('CartFolder', item.description)
        self.assertEquals('CartFolder', item.content_meta_type)
        self.assertEquals('addCartFolder', item.factory)
        self.assertEquals('view', item.immediate_view)
        self.assertEquals(True, item.global_allow)
        self.assertEquals(True, item.filter_content_types)
        self.assertEquals(('Cart',), item.allowed_content_types)
        self.assertEquals('view', item.default_view)
        self.assertEquals(('view', 'folder_tabular_view', 'folder_listing'), item.view_methods)
        aliases = {'edit': 'atct_edit', 'sharing': '@@sharing', '(Default)': '(dynamic view)', 'view': '(selected layout)'}
        self.assertEquals(aliases, item.getMethodAliases())
        # actions = [
        #     (action.title, action.id, action.getActionExpression(), action.visible, action.permissions) for action in item.listActions()
        # ]
        self.assertEquals(
            [
                ('View', 'view', 'string:${folder_url}/', True, (u'View',)),
                ('Edit', 'edit', 'string:${object_url}/edit', True, (u'Modify portal content',))
            ],
            [
                (action.title, action.id, action.getActionExpression(), action.visible, action.permissions) for action in item.listActions()
            ]
        )

    def test_cart_content_type(self):
        item = self.types.getTypeInfo('Cart')
        self.assertEquals('Cart', item.title)
        self.assertEquals('Cart', item.description)
        self.assertEquals('Cart', item.content_meta_type)
        self.assertEquals('addCart', item.factory)
        self.assertEquals('view', item.immediate_view)
        self.assertEquals(False, item.global_allow)
        self.assertEquals(True, item.filter_content_types)
        self.assertEquals(('CartProduct',), item.allowed_content_types)
        self.assertEquals('view', item.default_view)
        self.assertEquals(('view', 'folder_listing', 'folder_tabular_view'), item.view_methods)
        aliases = {'edit': 'atct_edit', 'sharing': '@@sharing', '(Default)': '(dynamic view)', 'view': '(selected layout)'}
        self.assertEquals(aliases, item.getMethodAliases())
        self.assertEquals(
            [
                ('View', 'view', 'string:${folder_url}/', True, (u'View',)),
                ('Edit', 'edit', 'string:${object_url}/edit', True, (u'Modify portal content',))
            ],
            [
                (action.title, action.id, action.getActionExpression(), action.visible, action.permissions) for action in item.listActions()
            ]
        )

    def test_cart_product_content_type(self):
        item = self.types.getTypeInfo('CartProduct')
        self.assertEquals('CartProduct', item.title)
        self.assertEquals('CartProduct', item.description)
        self.assertEquals('CartProduct', item.content_meta_type)
        self.assertEquals('addCartProduct', item.factory)
        self.assertEquals('view', item.immediate_view)
        self.assertEquals(False, item.global_allow)
        self.assertEquals(False, item.filter_content_types)
        self.assertEquals((), item.allowed_content_types)
        self.assertEquals('view', item.default_view)
        self.assertEquals(('view',), item.view_methods)
        aliases = {'edit': 'atct_edit', 'sharing': '@@sharing', '(Default)': '(dynamic view)', 'view': '(selected layout)'}
        self.assertEquals(aliases, item.getMethodAliases())
        self.assertEquals(
            [
                ('View', 'view', 'string:${object_url}', True, (u'View',)),
                ('Edit', 'edit', 'string:${object_url}/edit', True, (u'Modify portal content',))
            ],
            [
                (action.title, action.id, action.getActionExpression(), action.visible, action.permissions) for action in item.listActions()
            ]
        )

    ## propertiestool.xml
    def test_collective_cart_properties(self):
        ccp = getattr(self.properties, 'collective_cart_properties')
        self.assertEquals('Cart Properties', ccp.getProperty('title'))
        self.assertEquals('EUR', ccp.getProperty('currency'))
        self.assertEquals('', ccp.getProperty('currency_symbol'))
        self.assertEquals('Behind', ccp.getProperty('symbol_location'))
        self.assertEquals((), ccp.getProperty('content_types'))

    ## controlpanel.xml
    def test_configlet(self):
        act = [action for action in self.controlpanel.listActions() if action.id == 'collective_cart_config'][0]
        self.assertEquals(u'Cart Config', act.title)
        self.assertEquals("collective.cart.core", act.appId)

        try:
            ## Plone4
            self.assertEquals("string:$portal_url/maintenance_icon.png", act.icon_expr.text)
        except AttributeError:
            ## Plone3
            pass

        self.assertEquals("string:${portal_url}/@@cart-config", act.action.text)

    ## site_properties
    def test_not_searchable(self):
        self.failUnless('Cart' in self.site_properties.getProperty('types_not_searched'))
        self.failUnless('CartFolder' in self.site_properties.getProperty('types_not_searched'))
        self.failUnless('CartProduct' in self.site_properties.getProperty('types_not_searched'))

    def test_use_folder_tabs(self):
        try:
            self.failUnless('Cart' not in self.site_properties.getProperty('use_folder_tabs'))
            self.failUnless('CartFolder' not in self.site_properties.getProperty('use_folder_tabs'))
            self.failUnless('CartProduct' not in self.site_properties.getProperty('use_folder_tabs'))
        except TypeError:
            pass

    def test_typesLinkToFolderContentsInFC(self):
        self.failUnless('Cart' not in self.site_properties.getProperty('typesLinkToFolderContentsInFC'))
        self.failUnless('CartFolder' not in self.site_properties.getProperty('typesLinkToFolderContentsInFC'))
        self.failUnless('CartProduct' not in self.site_properties.getProperty('typesLinkToFolderContentsInFC'))

    ## navtree_properties
    def test_not_in_navtree(self):
        self.failUnless('Cart' in self.navtree_properties.getProperty('metaTypesNotToList'))
        self.failUnless('CartFolder' in self.navtree_properties.getProperty('metaTypesNotToList'))
        self.failUnless('CartProduct' in self.navtree_properties.getProperty('metaTypesNotToList'))

    ## catalog.xml
    def test_catalog_index(self):
        self.failUnless('uid' in self.catalog.indexes())
        self.failUnless('session_cart_id' in self.catalog.indexes())

    def test_metadata(self):
        self.failUnless('quantity' in self.catalog.schema())

    ## worlflows.xml
    def test_worlflow_installed(self):
        for item in ['cart_folder_default_workflow', 'cart_default_workflow', 'cart_product_default_workflow']:
            self.failUnless(item in self.workflow.objectIds())

    def test_cart_folder_workflow_chain(self):
        self.failUnless('cart_folder_default_workflow' in self.workflow.getChainForPortalType('CartFolder'))

    def test_cart_workflow_chain(self):
        self.failUnless('cart_default_workflow' in self.workflow.getChainForPortalType('Cart'))

    def test_cart_product_workflow_chain(self):
        self.failUnless('cart_product_default_workflow' in self.workflow.getChainForPortalType('CartProduct'))

    ## cart_folder_default_workflow definition.xml
    def test_cart_folder_default_workflow_definition_permissions(self):
        perms = ('Access contents information', 'List folder contents', 'Modify portal content', 'View', 'collective.cart.core: Add Cart')
        state = self.workflow.cart_folder_default_workflow.states.secured
        for perm in perms:
            self.failUnless(perm in self.workflow.cart_folder_default_workflow.permissions)
            self.assertEqual(0, state.getPermissionInfo(perm)['acquired'])
        secured_permission_roles = {
            'Modify portal content': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
            'Access contents information': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
            'List folder contents': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
            'View': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
             'collective.cart.core: Add Cart': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
        }
        self.assertEqual(secured_permission_roles, state.permission_roles)

    def test_cart_folder_default_workflow_definition_states(self):
        self.assertEqual(['secured'], self.workflow.cart_folder_default_workflow.states.objectIds())

    ## cart_default_workflow definition.xml
    def test_cart_default_workflow_definition_permissions(self):
        perms = ('Access contents information', 'List folder contents', 'Modify portal content', 'View', 'collective.cart.core: Add CartProduct')
        for perm in perms:
            self.failUnless(perm in self.workflow.cart_default_workflow.permissions)

    def test_cart_default_workflow_definition_states(self):
        states = ['canceled', 'shipped', 'charged', 'paid', 'created']
        for state in states:
            self.failUnless(state in self.workflow.cart_default_workflow.states.objectIds())
        items = dict(self.workflow.cart_default_workflow.states.objectItems())
        created = items.get('created')
        charged = items.get('charged')
        paid = items.get('paid')
        shipped = items.get('shipped')
        canceled = items.get('canceled')
        for item in ['charge', 'cancel']:
            self.failUnless(item in created.getTransitions())
        for item in ['pay', 'cancel', 'create']:
            self.failUnless(item in charged.getTransitions())
        for item in ['ship', 'cancel']:
            self.failUnless(item in paid.getTransitions())
        self.assertEqual((), shipped.getTransitions())
        self.assertEqual((), canceled.getTransitions())
        objs = items.values()
        perms = ('Access contents information', 'List folder contents', 'Modify portal content', 'View', 'collective.cart.core: Add CartProduct')
        for obj in objs:
            for perm in perms:
                self.assertEqual(0, obj.getPermissionInfo(perm)['acquired'])
        created_permission_roles = {
            'Modify portal content': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
           'List folder contents': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
            'Access contents information': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
            'View': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
             'collective.cart.core: Add CartProduct': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
        }
        self.assertEqual(created_permission_roles, created.permission_roles)
        other_permission_roles = {
            'Modify portal content': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
           'List folder contents': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
            'Access contents information': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
            'View': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
             'collective.cart.core: Add CartProduct': (
            ),
        }
        states.remove('created')
        objs = [items[state] for state in states]
        for obj in objs:
            self.assertEqual(other_permission_roles, obj.permission_roles)

    def test_cart_default_workflow_definition_transitions(self):
        transitions = ['cancel', 'pay', 'charge', 'create', 'ship']
        for transition in transitions:
            self.failUnless(transition in self.workflow.cart_default_workflow.transitions.objectIds())
        items = dict(self.workflow.cart_default_workflow.transitions.objectItems())
        charge = items.get('charge')
        pay = items.get('pay')
        ship = items.get('ship')
        cancel = items.get('cancel')
        create = items.get('create')
        self.assertEqual('charged', charge.new_state_id)
        self.assertEqual('paid', pay.new_state_id)
        self.assertEqual('shipped', ship.new_state_id)
        self.assertEqual('canceled', cancel.new_state_id)
        self.assertEqual('created', create.new_state_id)

    def test_cart_product_default_workflow_definition_states(self):
        states = ['editable_for_customer', 'not_editable_for_customer']
        for state in states:
            self.failUnless(state in self.workflow.cart_product_default_workflow.states.objectIds())
        items = dict(self.workflow.cart_product_default_workflow.states.objectItems())
        editable_for_customer = items.get('editable_for_customer')
        not_editable_for_customer = items.get('not_editable_for_customer')
        for item in ['fix']:
            self.failUnless(item in editable_for_customer.getTransitions())
        for item in ['unfix']:
            self.failUnless(item in not_editable_for_customer.getTransitions())
        objs = items.values()
        perms = ('Access contents information', 'Modify portal content', 'View')
        for obj in objs:
            for perm in perms:
                self.assertEqual(0, obj.getPermissionInfo(perm)['acquired'])
        editable_for_customer_permission_roles = {
            'Modify portal content': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
            'Access contents information': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
            'View': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            )
        }
        self.assertEqual(editable_for_customer_permission_roles, editable_for_customer.permission_roles)
        not_editable_for_customer_permission_roles = {
            'Modify portal content': (
                'Contributor',
                'Manager',
                'Site Administrator'
            ),
            'Access contents information': (
                'Anonymous',
                'Authenticated',
                'Contributor',
                'Manager',
                'Member',
                'Owner',
                'Site Administrator'
            ),
            'View': (
                'Contributor',
                'Manager',
                'Site Administrator'
            )
        }
        self.assertEqual(not_editable_for_customer_permission_roles, not_editable_for_customer.permission_roles)
        self.assertEqual(not_editable_for_customer_permission_roles, not_editable_for_customer.permission_roles)

    def test_cart_product_default_workflow_definition_transitions(self):
        transitions = ['fix', 'unfix']
        for transition in transitions:
            self.failUnless(transition in self.workflow.cart_product_default_workflow.transitions.objectIds())
        items = dict(self.workflow.cart_product_default_workflow.transitions.objectItems())
        fix = items.get('fix')
        unfix = items.get('unfix')
        self.assertEqual('not_editable_for_customer', fix.new_state_id)
        self.assertEqual('editable_for_customer', unfix.new_state_id)

    ## actions.xml
    def test_make_addable_to_cart(self):
        matc = self.actions.object_buttons.make_addable_to_cart
        self.assertEqual('Make Addable To Cart', matc.getProperty('title'))
        self.assertEqual('string:${globals_view/getCurrentObjectUrl}/@@make-addable-to-cart', matc.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("potentially-addable-but-not-addable-to-cart")()', matc.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), matc.getProperty('permissions'))
        self.assertEqual(True, matc.getProperty('visible'))

    def test_make_not_addable_to_cart(self):
        matc = self.actions.object_buttons.make_not_addable_to_cart
        self.assertEqual('Make Not Addable To Cart', matc.getProperty('title'))
        self.assertEqual('string:${globals_view/getCurrentObjectUrl}/@@make-not-addable-to-cart', matc.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("addable-to-cart")()', matc.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), matc.getProperty('permissions'))
        self.assertEqual(True, matc.getProperty('visible'))

    def test_editProduct(self):
        matc = self.actions.object.editProduct
        self.assertEqual('Edit Product', matc.getProperty('title'))
        self.assertEqual('string:${object_url}/@@edit-product', matc.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("addable-to-cart")()', matc.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), matc.getProperty('permissions'))
        self.assertEqual(True, matc.getProperty('visible'))

    def test_portlet(self):
        left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
        left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
        self.failUnless(u'Cart' in left_assignable.keys())

    ## Uninstalling
    def test_uninstall(self):
        self.installer.uninstallProducts(['collective.cart.core'])
        self.failUnless(not self.installer.isProductInstalled('collective.cart.core'))
        ids = [action.id for action in self.controlpanel.listActions()]
        self.failUnless('collective_cart_config' not in ids)
        self.failUnless(not hasattr(self.properties, 'collective_cart_properties'))
        for type in self.content_types:
            self.failIf(type in self.types.objectIds())
        left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
        left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
        self.failIf(u'Cart' in left_assignable.keys())
