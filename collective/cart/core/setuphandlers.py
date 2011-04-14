from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, getMultiAdapter
from zope.app.container.interfaces import INameChooser
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from collective.cart.core.portlets.cart import Assignment


def setupCartProperties(portal):
    names = ['Cart', 'CartFolder', 'CartProduct']
    for name in names:
        properties = getToolByName(portal, 'portal_properties')

        ## Site Properties
        site_properties = getattr(properties, 'site_properties')

        types_not_searched = list(
            site_properties.getProperty('types_not_searched'))
        if name not in types_not_searched:
            types_not_searched.append(name)
        site_properties.manage_changeProperties(
            types_not_searched=types_not_searched)

        ## Navtree Properties
        navtree_properties = getattr(properties, 'navtree_properties')
        types_not_listed = list(
            navtree_properties.getProperty('metaTypesNotToList'))
        if name not in types_not_listed:
            types_not_listed.append(name)
        navtree_properties.manage_changeProperties(
            metaTypesNotToList=types_not_listed)


def setupCartPortlet(portal):
        left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
        manager = getMultiAdapter((portal, left_column), IPortletAssignmentMapping)
        if 'cart' not in manager.keys():
            assignment = Assignment()
            chooser = INameChooser(manager)
            manager[chooser.chooseName(None, assignment)] = assignment


def setupVarious(context):

    if context.readDataFile('collective.cart.core_various.txt') is None:
        return

    portal = context.getSite()
    setupCartProperties(portal)
    setupCartPortlet(portal)
