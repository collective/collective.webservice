from Products.CMFCore.utils import UniqueObject
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass


class WebserviceTool (UniqueObject, SimpleItem):
    """ WebServiceTool  .... """
    id = 'webservice_tool'
    meta_type = 'Web Service Tool' 
    plone_tool = 1

    def method(self, id_webservice):
        """ method ... """
        pass

InitializeClass(WebserviceTool)
