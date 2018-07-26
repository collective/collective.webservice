# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility


def remove_old_fields(context):
    registry = queryUtility(IRegistry)
    try:
        del registry.records['collective.webservice.interfaces.IWebserviceSettings.defaultTimeout']
        del registry.records['collective.webservice.interfaces.IWebserviceSettings.memcachedAddress']
        del registry.records['collective.webservice.interfaces.IWebserviceSettings.memcachedCache']
        del registry.records['collective.webservice.interfaces.IWebserviceSettings.proxyInfo']
    except KeyError:
        pass
