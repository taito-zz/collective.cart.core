Introduction
============

collective.cart.core is yet another cart for Plone.
It makes any ATContentTypes addable to cart inspired by getpaid_ project.

.. _getpaid: http://pypi.python.org/pypi/Products.PloneGetPaid

* This package is still under active development and only suitable for certain use cases for now.

Currently tested with
---------------------

* Plone-3.3.5

* Plone-4.1b2

* Products.PloneFormGen-1.6.0 (Optional)

How To
------
Once you have quickinstalled the package to Plone Site:

1. Add Cart Folder to the site.

 * The cart will be stored here.
 * The location of the Cart Folder does not matter.
 * Do not add more than one Cart Folder to the site.
 * The multiple Cart Folder will be supported some time later...

2. Go to *Site Setup* >> *Cart Config*

 * Here you can set properties for product prices and content types which can be added to cart.
 * Lack of explanations here will be added some time later...

3. Make content type addable to cart.

 1. Go to some content type selected in *Cart Config*.
 2. *Action* >> *Make Addable To Cart*
 3. Edit the product values and Save.

 * Now the Add To Cart button is appeared under Title of View.
 * If you add the product to cart, cart portlet appears.
 * You can check teh cart contents by clicking cart in the cart portlet.
