Introduction
============

collective.cart.core is yet another cart for Plone.

It makes any ATContentTypes addable to cart.

* Inspired by getpaid_ project.

.. _getpaid: http://pypi.python.org/pypi/Products.PloneGetPaid

Tested with
---------------------

* Plone-4.2x

How To
------
Once you have quickinstalled the package to Plone Site:

1. Add Cart Folder to the site.

 * The cart will be stored here.
 * If you have multiple cart folder, the cart will be added to the upper closest cart folder of the hierarchy line.

2. Go to *Site Setup* >> *Cart Config*

 * Here you can set properties for product prices and content types which can be added to cart.

3. Make content type addable to cart.

 1. Go to some content type selected in *Cart Config*.
 2. *Action* >> *Make Addable To Cart*
 3. Edit the product values and Save.

 * Now the Add To Cart button is appeared under Title of View.
 * If you add the product to cart, cart portlet appears.
 * You can check the cart contents by clicking cart in the cart portlet.
