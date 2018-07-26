# -*- coding: utf-8 -*-
from AccessControl import allow_class
from AccessControl import allow_module
from AccessControl import ModuleSecurityInfo
from zope.i18nmessageid import MessageFactory


# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

WebserviceMessageFactory = MessageFactory('collective.webservice')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    tipos = """
        voidType
        stringType
        untypedType
        IDType
        NCNameType
        NameType
        ENTITYType
        IDREFType
        languageType
        NMTOKENType
        QNameType
        tokenType
        normalizedStringType
        CDATAType
        booleanType
        decimalType
        floatType
        doubleType
        durationType
        timeDurationType
        dateTimeType
        recurringInstantType
        timeInstantType
        timePeriodType
        timeType
        dateType
        gYearMonthType
        gYearType
        centuryType
        yearType
        gMonthDayType
        recurringDateType
        gMonthType
        monthType
        gDayType
        recurringDayType
        hexBinaryType
        base64BinaryType
        base64Type
        binaryType
        anyURIType
        uriType
        uriReferenceType
        NOTATIONType
        ENTITIESType
        IDREFSType
        NMTOKENSType
        integerType
        nonPositiveIntegerType
        non_Positive_IntegerType
        negativeIntegerType
        negative_IntegerType
        longType
        intType
        shortType
        byteType
        nonNegativeIntegerType
        non_Negative_IntegerType
        unsignedLongType
        unsignedIntType
        unsignedShortType
        unsignedByteType
        positiveIntegerType
        positive_IntegerType
        compoundType
        structType
        headerType
        bodyType
        arrayType
        typedArrayType
    """

    tipos = [t.strip() for t in tipos.split('\n') if t.strip()]

    product_globals = globals()

    for t in tipos:
        dotted_name = 'SOAPpy.Types.' + t
        parts = dotted_name.split('.')
        m_name = '.'.join(parts[:-1])
        k_name = parts[-1]
        ModuleSecurityInfo(m_name).declarePublic(t)
        module = __import__(m_name, product_globals, locals(), [k_name])
        klass = getattr(module, k_name)
        allow_class(klass)

    allow_module('xml.parsers.expat')

    ModuleSecurityInfo('App.Common').declarePublic('rfc1123_date')
