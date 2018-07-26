# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


version = '0.6'

setup(name='collective.webservice',
      version=version,
      description='Add-on to work with webservices.',
      long_description=open('README.rst').read() + '\n' + open(os.path.join('docs', 'HISTORY.txt')).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          'Framework :: Plone',
          'Programming Language :: Python',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ],
      keywords='plone webservices',
      author='Fabio Surrage,Fabiano Weimar',
      author_email='fabiosurrage@gmail.com,xiru@xiru.com',
      url='http://github.com/collective/collective.webservice',
      license='GPLv2',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'SOAPpy',
          'suds',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[],
      paster_plugins=[],
      )
