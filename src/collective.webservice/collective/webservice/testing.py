from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig


class CollectiveWebservice(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.webservice
        xmlconfig.file('configure.zcml',
			collective.webservice,
			context=configurationContext
		)

	def setUpPloneSite(self, portal):
		applyProfile(portal, 'collective.webservice:default')

COLLECTIVE_WEBSERVICE_FIXTURE = CollectiveWebservice()
COLLECTIVE_WEBSERVICE_INTEGRATION_TESTING = IntegrationTesting(
	bases=(COLLECTIVE_WEBSERVICE_FIXTURE,),
	name="Collective:Integration"
	)

