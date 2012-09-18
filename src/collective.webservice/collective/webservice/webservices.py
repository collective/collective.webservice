# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from restful_lib import Connection

#import pdb
from plone.memoize.instance import memoize

import simplejson
import urllib
import SOAPpy
from SOAPpy import SOAPProxy
import sys
from types import *
from zLOG import LOG, INFO
DEBUG_1 = 0
DEBUG_2 = 0
DEBUG_3 = 0
TIMEOUT = 60


class Webservices(BrowserView):
    """View"""

   # def teste(self):
        #pdb.set_trace()

    def webservice_caller(self, wsdl, metodo, parametros, timeout = TIMEOUT, map = {}):

        SOAPpy.Config.debug = DEBUG_1

        if DEBUG_1:
            LOG('CCOLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
               (wsdl, metodo, repr(parametros), timeout, repr(map)))

        if isinstance(parametros, dict) and parametros.get('timeout', None) is not None:
            timeout = parametros['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = SOAPpy.WSDL.Proxy(wsdl, timeout=timeout)

    #    SOAPpy.Config.dumpSOAPOut = 1
    #    SOAPpy.Config.dumpSOAPIn = 1

        return self.result_webservice(wsdl, metodo, parametros, timeout, map, p, DEBUG_1)

    def webservice_caller_axis(self, wsdl, metodo, parametros, timeout=TIMEOUT, map={}, v_namespace='', v_soapaction=''):

        SOAPpy.Config.debug = DEBUG_2

        if DEBUG_2:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_axis. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
               (wsdl, metodo, repr(parametros), timeout, repr(map)))

        if isinstance(parametros, dict) and parametros.get('timeout', None) is not None:
            timeout = parametros['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, timeout=timeout)

        #p.config.dumpSOAPOut = 1
        #p.config.dumpSOAPIn = 1

        # return p.HelloWorld("nom")

        return self.result_webservice(wsdl, metodo, parametros, timeout, map, p, DEBUG_2)

    def webservice_caller_proxy(self, wsdl, metodo, parametros, timeout=TIMEOUT, map={}, v_namespace='', v_soapaction=''):

        SOAPpy.Config.debug = DEBUG_3

        if DEBUG_3:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_externo. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
               (wsdl, metodo, repr(parametros), timeout, repr(map)))

        if isinstance(parametros, dict) and parametros.get('timeout', None) is not None:
            timeout = parametros['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, http_proxy='10.1.1.46:8080', timeout=timeout)

        # p.config.dumpSOAPOut = 1
        # p.config.dumpSOAPIn = 1

        # return p.HelloWorld("nom")

        return self.result_webservice(wsdl, metodo, parametros, timeout, map, p, DEBUG_3)

    def result_webservice(self, wsdl, metodo, parametros, timeout, map, p, DEBUG):

        ret = None

        if isinstance(parametros, dict):
            ret = getattr(p, metodo)(**parametros)
        else:
            if not isinstance(parametros, tuple):
                parametros = (parametros,)
            ret = getattr(p, metodo)(*parametros)

        if DEBUG:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'End of method. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
              (wsdl, metodo, repr(parametros), timeout, repr(map)))

        if type(ret) == type(u'a'):
            return ret
        else:
            try:
                for x in ret:
                    for k in x._keys():
                        if type(x[k]) == type('a'):
                            u = self.corrige_encoding(x[k])
                            #u = unicode(x[k],'iso-8859-1').encode('utf-8')
                            x._placeItem(k, u, 0, 0)
                return ret
            except:
                return ret

    def restful_caller(self, url, metodo, parametros, http_metodo):
        try:
            conn = Connection(url)
        except:
            return 'Cant connect with ' + url
        ret = None
        if http_metodo.upper() == 'GET':
            try:
                ret = conn.request_get(resource=metodo, args=parametros, headers={'Content-type': 'text/xml', 'Accept': 'text/xml'})
            except:
                ret = 'Problem with method ' + metodo
        return ret

    def restful_Json_caller(self, url, parametros):
        url = url + '?' + urllib.urlencode(parametros)
        result = simplejson.load(urllib.urlopen(url))
        return result

    def isPublic(self, name):
        return name[0] != '_'

    def corrige_encoding(self, object, level=0):
        if level > 10:
            return object
        if isinstance(object, faultType):
            pass
        elif isinstance(object, arrayType):
            for k in range(len(object)):
                object[k] = simplify(object[k], level=level + 1)
            return object
        elif isinstance(object, compoundType) or isinstance(object, structType) or type(object) == DictType:
            for k in object.keys():
                if self.isPublic(k):
                    object[k] = simplify(object[k], level=level + 1)
            return object
        elif type(object) == list:
            for k in range(len(object)):
                object[k] = simplify(object[k])
            return object
        elif type(object) == type(''):
            return unicode(object, 'iso-8859-1').encode('utf-8')
        elif type(object) == type(u''):
            return object.encode('utf-8')
        else:
            return object
