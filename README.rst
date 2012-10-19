**********************
collective.webservices
**********************

.. contents:: Table of Contents

Introduction
------------

A collection of methods to integrate Plone with webservices. Under development.

The product provides a collection of methods to call some types of webservices:

- webservice_caller(wsdl, method, parameters, timeout=TIMEOUT, map={})
- webservice_caller_axis(wsdl, method, parameters, timeout=TIMEOUT, map={}, v_namespace='', v_soapaction='')
- webservice_caller_proxy(wsdl, method, parameters, timeout=TIMEOUT, map={}, v_namespace='', v_soapaction='')
- restful_caller(url, method, parameters, http_method)
- restful_Json_caller(url, parameters)
- call_webservice(wsdl, method, parameters, timeout)

Installation
------------


How to use
----------

You can call the ws view and use its methods from any Sprypt Python or Zope Page Template.
You you need to use the methods within another product or type, junt import collective.webservice and use it.

Examples of use
---------------

1. In a python script:

2. In a ZPT:

3. Within another product:

Have an idea? Found a bug? Let us know by `opening a support ticket`_.


