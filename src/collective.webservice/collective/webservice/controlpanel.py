from plone.z3cform import layout

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from collective.webservice.interfaces import IWebserviceSettings
from collective.webservice import WebserviceMessageFactory as _

class WebserviceControlPanelForm(RegistryEditForm):
    schema = IWebserviceSettings
    
    label = _(u"Webservices Control Panel")
    
WebserviceControlPanelView = layout.wrap_form(WebserviceControlPanelForm, ControlPanelFormWrapper)
