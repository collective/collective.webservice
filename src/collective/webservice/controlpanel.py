# -*- coding: utf-8 -*-
from collective.webservice import WebserviceMessageFactory as _
from collective.webservice.interfaces import IWebserviceSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout


class WebserviceControlPanelForm(RegistryEditForm):
    schema = IWebserviceSettings

    label = _(u'Webservices Control Panel')


WebserviceControlPanelView = layout.wrap_form(WebserviceControlPanelForm, ControlPanelFormWrapper)
