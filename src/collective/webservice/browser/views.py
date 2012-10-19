import json
from zope.interface import implements
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.Five import BrowserView
from collective.webservice.interfaces import IWS
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from collective.webservice.interfaces import IWebserviceSettings
from restful_lib import Connection
import simplejson
import urllib
import SOAPpy
from SOAPpy import SOAPProxy
from suds.client import Client
import sys
from types import *
from zLOG import LOG, INFO
DEBUG_1 = 0
DEBUG_2 = 0
DEBUG_3 = 0
TIMEOUT = 60  # Setting Default Timeout to 60 seconds


class WSJson(grok.View):
    """ A view that calls a webservice and return json.
    """

    grok.context(INavigationRoot)
    grok.name('wsjson')
    grok.require('zope2.View')

    def render(self):
        """ Return the list of WebServices
        """
        return "Im here!"
        ## TODO: Calling this view shows the configuration os all Webservices (Webservices Control Panel)


class WSView(BrowserView):
    """ A view that calls a webservice and return the suds output.
    """

    implements(IWS)

    def webservice_caller(self, wsdl, method, parameters, timeout=TIMEOUT, map={}):

        SOAPpy.Config.debug = DEBUG_1

        if DEBUG_1:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
               (wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = SOAPpy.WSDL.Proxy(wsdl, timeout=timeout)

    #    SOAPpy.Config.dumpSOAPOut = 1
    #    SOAPpy.Config.dumpSOAPIn = 1

        return self.result_webservice(wsdl, method, parameters, timeout, map, p, DEBUG_1)

    def webservice_caller_axis(self, wsdl, method, parameters, timeout=TIMEOUT, map={}, v_namespace='', v_soapaction=''):

        SOAPpy.Config.debug = DEBUG_2

        if DEBUG_2:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_axis. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
               (wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, timeout=timeout)

        #p.config.dumpSOAPOut = 1
        #p.config.dumpSOAPIn = 1

        # return p.HelloWorld("nom")

        return self.result_webservice(wsdl, method, parameters, timeout, map, p, DEBUG_2)

    def webservice_caller_proxy(self, wsdl, method, parameters, timeout=TIMEOUT, map={}, v_namespace='', v_soapaction=''):

        SOAPpy.Config.debug = DEBUG_3

        if DEBUG_3:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_externo. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
               (wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, http_proxy=MY_PROXY, timeout=timeout)

        # p.config.dumpSOAPOut = 1
        # p.config.dumpSOAPIn = 1

        # return p.HelloWorld("nom")

        return self.result_webservice(wsdl, method, parameters, timeout, map, p, DEBUG_3)

    def result_webservice(self, wsdl, method, parameters, timeout, map, p, DEBUG):

        ret = None

        if isinstance(parameters, dict):
            ret = getattr(p, method)(**parameters)
        else:
            if not isinstance(parameters, tuple):
                parameters = (parameters,)
            ret = getattr(p, method)(*parameters)

        if DEBUG:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'End of method. wsdl: %s, method: %s, parameters: %s, timeout: %d, map: %s' % \
              (wsdl, method, repr(parameters), timeout, repr(map)))

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

    def restful_caller(self, url, method, parameters, http_method):
        try:
            conn = Connection(url)
        except:
            return 'Cant connect with ' + url
        ret = None
        if http_method.upper() == 'GET':
            try:
                ret = conn.request_get(resource=method, args=parameters, headers={'Content-type': 'text/xml', 'Accept': 'text/xml'})
            except:
                ret = 'Problem with method ' + method
        return ret
        # TODO : POST, UPDATE and DELETE Methods

    def restful_Json_caller(self, url, parameters):
        url = url + '?' + urllib.urlencode(parameters)
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

    def call_webservice(self, **kwargs):
        registry = queryUtility(IRegistry)
        if registry is None:
            PROXY = None
            TIMEOUT = 60
        else:
            settings = registry.forInterface(IWebserviceSettings, check=False)
            ## TODO : Test if not set
            PROXY = settings.proxyInfo[0]
            TIMEOUT = settings.defaultTimeout[0]

        wsdl = kwargs.get('wsdl', '')
        method = kwargs.get('method', '')
        timeout = kwargs.get('timeout', TIMEOUT)
        parameters = kwargs.get('parameters')
        client = Client(wsdl, timeout=timeout)
        if PROXY:
            d = dict(http=PROXY, https=PROXY)
            client.set_options(proxy=d)
        #client.set_options(retxml=True)
        if isinstance(parameters, dict):
            ret = getattr(client.service, method)(**parameters)
        else:
            if not isinstance(parameters, tuple):
                parameters = (parameters,)
            ret = getattr(client.service, method)(*parameters)

        return ret
