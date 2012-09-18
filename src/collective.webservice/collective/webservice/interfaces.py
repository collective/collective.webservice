# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema

from collective.webservice import WebserviceMessageFactory as _


class IWebserviceSettings(Interface):
    webserviceInfo = schema.Tuple(
            title=_(u"Information about WebServices"),
            description=_(u"Information about WebServices"),
            value_type=schema.TextLine(),
            required=False,
            )
    proxyInfo = schema.Tuple(
            title=_(u"Information about Proxy"),
            description=_(u"Enter your proxy address like http://your.proxy:8080"),
            value_type=schema.Text(),
            required=False,
            )


class Webservices(Interface):

    def webservice_caller(wsdl, method, parameters, timeout, map):
        """ Method for use with a standart webservice """

    def webservice_caller_axis(wsdl, method, parameters, timeout, map, v_namespace, v_soapaction):
        """ Method for use with a axis webservice """

    def webservice_caller_proxy(wsdl, method, parameters, timeout, map, v_namespace, v_soapaction):
        """ Method for use with a axis webservice behind a proxy """

    def restful_caller(url, method, parameter, http_method):
        """ Method for use with REST webservices """

    def restful_Json_caller(url, parameters):
        """ Method for use with REST webservices - returns Json """

    def corrige_encoding(object, level):
        """ Method for fix encode problems """

    def isPublic(name):
        """ """
