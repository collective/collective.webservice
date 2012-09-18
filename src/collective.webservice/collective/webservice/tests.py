# -*- coding: utf-8 -*-
import unittest
from collective.webservice.testing import COLLECTIVE_WEBSERVICE_INTEGRATION_TESTING
from collective.webservice.config import PROJECTNAME


class TestSetup(unittest.TestCase):
    layer = COLLECTIVE_WEBSERVICE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))


