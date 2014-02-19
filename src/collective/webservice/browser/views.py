# -*- coding: utf-8 -*-
import json
import hashlib
import memcache
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
import urllib2
import socket
import SOAPpy
from SOAPpy import SOAPProxy
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import sys
from types import *
from suds.sudsobject import asdict
from suds.sudsobject import Object as SudsObject
import cPickle as pickle

try:
    import threading
    thread_local = threading.local()
except ImportError:
    import zope.thread
    thread_local = zope.thread.local()

from zLOG import LOG, INFO
DEBUG_1 = 0
DEBUG_2 = 0
DEBUG_3 = 0
TIMEOUT = 20  # Setting Default Timeout to 20 seconds


class WSJson(grok.View):
    """ A view that calls a webservice and return json.
    """

    grok.context(INavigationRoot)
    grok.name('wsjson')
    grok.require('zope2.View')

    def render(self):
        """ Return the list of WebServices
        """
        registry = queryUtility(IRegistry)
        ret = ''
        if registry is not None:
            settings = registry.forInterface(IWebserviceSettings, check=False)
            position = 0
            for i in settings.wsdlAddress:
                ret += str(position) + ' - ' + str(i) + '\n'
                position += 1
            return ret
        else:
            return "Registry values not set"


class WSView():
    """ A view that calls a webservice and return the suds output.
    """

    implements(IWS)

    def webservice_caller(self, wsdl, method, parameters, timeout=TIMEOUT, map={}):

        SOAPpy.Config.debug = DEBUG_1

        if DEBUG_1:
            LOG('COLLECTIVE.WEBSERVICE', INFO,
                'Start of method webservice_caller. wsdl: %s, method: %s, parameters: %s, \
                timeout: %d, map: %s' % (wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = thread_local.client = SOAPpy.WSDL.Proxy(wsdl, timeout=timeout)

    #    SOAPpy.Config.dumpSOAPOut = 1
    #    SOAPpy.Config.dumpSOAPIn = 1

        return self.result_webservice(wsdl, method, parameters, timeout, map, p, DEBUG_1)

    def webservice_caller_axis(self, wsdl, method, parameters, timeout=TIMEOUT,
                               map={}, v_namespace='', v_soapaction=''):

        SOAPpy.Config.debug = DEBUG_2

        if DEBUG_2:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_axis. wsdl: %s, method: %s, \
                parameters: %s, timeout: %d, map: %s' % (wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = thread_local.client = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, timeout=timeout)

        #p.config.dumpSOAPOut = 1
        #p.config.dumpSOAPIn = 1

        # return p.HelloWorld("nom")

        return self.result_webservice(wsdl, method, parameters, timeout, map, p, DEBUG_2)

    def webservice_caller_proxy(self, wsdl, method, parameters, timeout=TIMEOUT,
                                map={}, v_namespace='', v_soapaction=''):

        SOAPpy.Config.debug = DEBUG_3

        if DEBUG_3:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_externo. wsdl: %s, method: %s, \
                parameters: %s, timeout: %d, map: %s' % (wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = map

        p = thread_local.client = SOAPProxy(wsdl, namespace=v_namespace,
                                            soapaction=v_soapaction, http_proxy=MY_PROXY, timeout=timeout)

        # p.config.dumpSOAPOut = 1
        # p.config.dumpSOAPIn = 1

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
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'End of method. wsdl: %s, method: %s, parameters: %s, timeout: %d, \
                map: %s' % (wsdl, method, repr(parameters), timeout, repr(map)))

        return ret

    def restful_caller(self, url, method, parameters, http_method):
        try:
            conn = Connection(url)
        except:
            return 'Cant connect with ' + url
        ret = None
        if http_method.upper() == 'GET':
            try:
                ret = conn.request_get(resource=method, args=parameters,
                                       headers={'Content-type': 'text/xml', 'Accept': 'text/xml'})
            except:
                ret = 'Problem with method ' + method
        return ret
        # TODO : POST, UPDATE and DELETE Methods

    def restful_Json_caller(self, url, method, parameters, timeout=30):

        if url.endswith('/'):
            url = url + method
        else:
            url = url + '/' + method

        if len(parameters) > 0:
            url = "%s?%s" % (url, urllib.urlencode(parameters))

        result = simplejson.load(urllib.urlopen(url))
        return result

    def call_webservice(self, **kwargs):
        registry = queryUtility(IRegistry)
        if registry is None:
            PROXY = None
            DEFAULT_TIMEOUT = 30
            DEFAULT_CACHE = 600
            MEMCACHED = None
        else:
            settings = registry.forInterface(IWebserviceSettings, check=False)
            # Setting PROXY
            if settings.proxyInfo:
                PROXY = settings.proxyInfo[0]
            else:
                PROXY = None
            # Setting default TIMEOUT
            if settings.defaultTimeout:
                DEFAULT_TIMEOUT = settings.defaultTimeout[0]
            else:
                DEFAULT_TIMEOUT = 30
            # Setting MEMCACHED address
            if settings.memcachedAddress:
                MEMCACHED = settings.memcachedAddress[0]
            else:
                MEMCACHED = None
            # Setting default Memcached CACHE
            if settings.memcachedAddress:
                DEFAULT_CACHE = settings.memcachedCache[0]
            else:
                DEFAULT_CACHE = 600

        wsdl = kwargs.get('wsdl', '')
        method = kwargs.get('method', '')
        timeout = kwargs.get('timeout', TIMEOUT)
        cache = kwargs.get('cache', DEFAULT_CACHE)
        parameters = kwargs.get('parameters')

        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        doctor = ImportDoctor(imp)
        client = thread_local.client = Client(wsdl, timeout=timeout, doctor=doctor)

        if PROXY:
            d = dict(http=PROXY, https=PROXY)
            client.set_options(proxy=d)

        if MEMCACHED:
            # calcule the cache key
            m = hashlib.md5()
            m.update(repr(kwargs))
            key = m.hexdigest()

            # create the memcached connection in new thread
            mc = thread_local.client = memcache.Client([MEMCACHED])

            value = mc.get(key)

            if value is not None:
                return value

        if isinstance(parameters, dict):
            ws_value = getattr(client.service, method)(**parameters)
        else:
            if not isinstance(parameters, tuple):
                parameters = (parameters,)
            ws_value = getattr(client.service, method)(*parameters)

        value = node_to_dict(ws_value, {})

        if isinstance(value, dict) and len(value.keys()) == 1:
            value = value[value.keys()[0]]

        if MEMCACHED:

            if value is not None:

                if value == -1 or value == [] or value == {}:
                    mc.delete(key)
                    return value

                if value:
                    return value

                else:
                    mc.delete(key)
                    return value
            else:
                mc.set(key, repr(value), int(cache))

        return value


def node_to_dict(node, node_data):
    """
    http://stackoverflow.com/questions/2412486/serializing-a-suds-object-in-python
    Author: Rogerio Hilbert Lima
    """

    if hasattr(node, '__keylist__'):
        keys = node.__keylist__
        for key in keys:
            if isinstance(node[key], list):
                lkey = key.replace('[]', '')
                node_data[lkey] = node_to_dict(node[key], [])
            elif hasattr(node[key], '__keylist__'):
                node_data[key] = node_to_dict(node[key], {})
            else:
                if isinstance(node_data, list):
                    node_data.append(node[key])
                else:
                    node_data[key] = node[key]
        return node_data
    else:
        if isinstance(node, list):
            node_data = []
            for lnode in node:
                node_data.append(node_to_dict(lnode, {}))
            return node_data
        else:
            return node

    node_to_dict(instance, node_data)
    return node_data
