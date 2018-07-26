# -*- coding: utf-8 -*-
from collective.webservice import WebserviceMessageFactory as _
from zope import schema
from zope.interface import Interface


class IWebserviceSettings(Interface):

    wsdlAddress = schema.Tuple(
        title=_(u'List os WSDLs address'),
        description=_(u'For each webservice that you will use, enter a wsdl url here'),
        value_type=schema.Text(),
        required=False,
    )
