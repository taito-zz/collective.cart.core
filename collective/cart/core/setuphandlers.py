from Products.CMFCore.utils import getToolByName


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


def setupVarious(context):

    if context.readDataFile('collective.cart.core_various.txt') is None:
        return

    portal = context.getSite()
    setupCartProperties(portal)
