# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema

from collective.webservice import WebserviceMessageFactory as _


class IWebserviceSettings(Interface):
    proxyInfo = schema.Tuple(
            title=_(u"Information about Proxy"),
            description=_(u"Enter your proxy address like your.proxy:8080"),
            value_type=schema.TextLine(),
            required=False,
            )

    memcachedAddress = schema.Tuple(
            title=_(u"Information about Memcached"),
            description=_(u"Enter the adress of your memcached server like your.proxy:8080"),
            value_type=schema.TextLine(),
            required=False,
            )

    memcachedCache = schema.Tuple(
            title=_(u"Information about Memcached"),
            description=_(u"Enter the default time of expiration of your memcached cache in seconds"),
            value_type=schema.TextLine(),
            default=('600',),
            required=False,
            )

    defaultTimeout = schema.Tuple(
            title=_(u"Information about default timeout for webservices"),
            description=_(u"Enter the default timeout in seconds for the webservices"),
            value_type=schema.TextLine(),
            default=('30',),
            required=False,
            )

    wsdlAddress = schema.Tuple(
            title=_(u"List os WSDLs address"),
            description=_(u"For each webservice that you will use, enter a wsdl url here"),
            value_type=schema.Text(),
            required=False,
            )


class IWS(Interface):
    """A webservices runner.
    """

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

    def call_webservice(**kwargs):
        """ Method in SUDS to call a webservice """
