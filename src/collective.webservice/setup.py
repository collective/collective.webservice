from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.webservice',
      version=version,
      description="Tool to work with WebServices",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Fabio Surrage de Medeiros',
      author_email='fabiosurrage@gmail.com',
      url='http://github.com/collective/collective.webservice',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'Products.CMFPlone',
          'plone.app.registry',
          'plone.app.z3cform',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing', ]
          },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
