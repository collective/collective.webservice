# -*- coding: utf-8 -*-
from collective.webservice.interfaces import IWebserviceSettings
from plone import api
from Products.Five import BrowserView
from SOAPpy import SOAPProxy
from suds.client import Client
from suds.sax.text import Text
from suds.xsd.doctor import Import
from suds.xsd.doctor import ImportDoctor
from zLOG import INFO
from zLOG import LOG

import os
import SOAPpy
import ssl
import threading


DEBUG_1 = 0
DEBUG_2 = 0
DEBUG_3 = 0
DEFAULT_TIMEOUT = 20
thread_local = threading.local()


class WSJson(BrowserView):
    """ A view that calls a webservice and return json."""

    def render(self):
        """ Return the list of WebServices"""
        ret = []
        wsdl_address = api.portal.get_registry_record('wsdlAddress', IWebserviceSettings, default=[])
        position = 0
        for i in wsdl_address:
            ret += str(position) + ' - ' + str(i) + '\n'
            position += 1
        return ret


class WSView:
    """ A view that calls a webservice and return the suds output."""

    def webservice_caller(self, wsdl, method, parameters, timeout=DEFAULT_TIMEOUT, w_map={}, ignore_ssl=False):

        SOAPpy.Config.debug = DEBUG_1

        if DEBUG_1:
            LOG('COLLECTIVE.WEBSERVICE', INFO,
                'Start of method webservice_caller. wsdl: {0}, method: {1}, parameters: {2}, \
                timeout: {3}, w_map: {4}'.format(wsdl, method, repr(parameters), timeout, repr(w_map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = w_map

        if ignore_ssl:
            ssl._create_default_https_context = ssl._create_unverified_context

        p = thread_local.client = SOAPpy.WSDL.Proxy(wsdl, timeout=timeout)

        # SOAPpy.Config.dumpSOAPOut = 1
        # SOAPpy.Config.dumpSOAPIn = 1

        return self.result_webservice(wsdl, method, parameters, timeout, w_map, p, DEBUG_1)

    def webservice_caller_axis(self, wsdl, method, parameters, timeout=DEFAULT_TIMEOUT, w_map={}, v_namespace='',
                               v_soapaction='', ignore_ssl=False):

        SOAPpy.Config.debug = DEBUG_2

        if DEBUG_2:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_axis. wsdl: {0}, method: {1}, \
                parameters: {2}, timeout: {3}, w_map: {4}'.format(wsdl, method, repr(parameters), timeout, repr(map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = w_map

        if ignore_ssl:
            ssl._create_default_https_context = ssl._create_unverified_context

        p = thread_local.client = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, timeout=timeout)

        # p.config.dumpSOAPOut = 1
        # p.config.dumpSOAPIn = 1

        return self.result_webservice(wsdl, method, parameters, timeout, w_map, p, DEBUG_2)

    def webservice_caller_proxy(self, wsdl, method, parameters, timeout=DEFAULT_TIMEOUT, w_map={}, v_namespace='',
                                v_soapaction='', http_proxy='', ignore_ssl=False):

        SOAPpy.Config.debug = DEBUG_3

        if DEBUG_3:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'Start of method webservice_caller_externo. wsdl: {0}, method: {1}, \
                parameters: {2}, timeout: {3}, w_map: {4}'.format(wsdl, method, repr(parameters), timeout, repr(w_map)))

        if isinstance(parameters, dict) and parameters.get('timeout', None) is not None:
            timeout = parameters['timeout']

        SOAPpy.Config.methodAttributeParameters = w_map

        if ignore_ssl:
            ssl._create_default_https_context = ssl._create_unverified_context

        http_proxy = os.environ.get('HTTP_PROXY', http_proxy)

        p = thread_local.client = SOAPProxy(wsdl, namespace=v_namespace, soapaction=v_soapaction, http_proxy=http_proxy,
                                            timeout=timeout)

        # p.config.dumpSOAPOut = 1
        # p.config.dumpSOAPIn = 1

        return self.result_webservice(wsdl, method, parameters, timeout, w_map, p, DEBUG_3)

    def result_webservice(self, wsdl, method, parameters, timeout, w_map, p, DEBUG):

        ret = None

        if isinstance(parameters, dict):
            ret = getattr(p, method)(**parameters)
        else:
            if not isinstance(parameters, tuple):
                parameters = (parameters,)
            ret = getattr(p, method)(*parameters)

        if DEBUG:
            LOG('COLLECTIVE.WEBSERVICE', INFO, 'End of method. wsdl: {0}, method: {1}, parameters: {2}, timeout: {3}, \
                w_map: {4}'.format(wsdl, method, repr(parameters), timeout, repr(w_map)))

        return ret

    def call_webservice(self, **kwargs):
        """Client Suds """

        wsdl = kwargs.get('wsdl', '')
        method = kwargs.get('method', '')
        timeout = kwargs.get('timeout', DEFAULT_TIMEOUT)
        proxy = kwargs.get('proxy', False)
        http_proxy = kwargs.get('http_proxy', '')
        parameters = kwargs.get('parameters')

        if kwargs.get('ignore_ssl', ''):
            ssl._create_default_https_context = ssl._create_unverified_context

        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        doctor = ImportDoctor(imp)
        client = Client(wsdl, timeout=timeout, doctor=doctor)

        if proxy:
            http_proxy = os.environ.get('HTTP_PROXY', http_proxy)
            client.set_options(proxy=http_proxy)

        if isinstance(parameters, dict):
            ws_value = getattr(client.service, method)(**parameters)
        else:
            if not isinstance(parameters, tuple):
                parameters = (parameters,)
            ws_value = getattr(client.service, method)(*parameters)

        value = node_to_dict(ws_value, {})

        if isinstance(value, dict) and len(value.keys()) == 1:
            value = value[value.keys()[0]]

        return value


def node_to_dict(node, node_data):
    """
    http://stackoverflow.com/questions/2412486/serializing-a-suds-object-in-python
    Author: Rogerio Hilbert Lima
    """
    if getattr(node, '__keylist__', None):
        keys = node.__keylist__
        for key in keys:
            if isinstance(node[key], list):
                lkey = key.replace('[]', '')
                node_data[lkey] = node_to_dict(node[key], [])
            elif getattr(node[key], '__keylist__', None):
                node_data[key] = node_to_dict(node[key], {})
            else:
                if isinstance(node_data, list):
                    node_data.append(node[key])
                else:
                    if isinstance(node[key], Text):
                        node_data[key] = str(node[key])
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
