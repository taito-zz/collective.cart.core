from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('collective', 'cart', 'core', 'version.txt').strip()

long_description = (
    open("README.txt").read() + "\n" +
    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
    open(os.path.join("docs", "HISTORY.txt")).read() + "\n" +
    open(os.path.join("docs", "CONTRIBUTORS.txt")).read() + "\n" +
    open(os.path.join("docs", "CREDITS.txt")).read()
    )

setup(name='collective.cart.core',
      version=version,
      description="Yet another cart for Plone.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Taito Horiuchi',
      author_email='taito.horiuchi@gmail.com',
      url='https://github.com/taito/collective.cart.core',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.cart'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Products.CMFPlone',
          'hexagonit.testing',
          'mock',
          'setuptools',
          'unittest2',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
