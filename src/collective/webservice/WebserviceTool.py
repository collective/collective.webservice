# -*- coding: utf-8 -*-
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import UniqueObject


class WebserviceTool (UniqueObject, SimpleItem):
    """ WebServiceTool  .... """
    id = 'webservice_tool'
    meta_type = 'Web Service Tool'
    plone_tool = 1

    def method(self, id_webservice):
        """ method ... """
        pass


InitializeClass(WebserviceTool)
