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


class Webservices(Interface):

    def webservice_caller(wsdl, metodo, parametros, timeout, map):
        """ Method for use with a standart webservice """

    def webservice_caller_axis(wsdl, metodo, parametros, timeout, map, v_namespace, v_soapaction):
        """ Method for use with a axis webservice """

    def webservice_caller_proxy(wsdl, metodo, parametros, timeout, map, v_namespace, v_soapaction):
        """ Method for use with a axis webservice behind a proxy """

    def restful_caller(url,metodo,parametro,http_metodo):
        """ Method for use with REST webservices """

    def restful_Json_caller(url, parametros):
        """ Method for use with REST webservices - returns Json """

    def corrige_encoding(object, level):
        """ Method para corrigir encoding """

    def isPublic(name):
        """ """
