import json
from presidio_analyzer import RemoteRecognizer, RecognizerResult

from presidio_analyzer.predefined_recognizers.text_analytics_dal \
    import TextAnalyticsDal


TYPES_MAPPING = {
        'Product': 'COMPUTER_PRODUCTS',
        'DateTime': 'DATE_TIME',
        'PersonType': 'PERSON_TYPE',
        'Credit Card': 'CREDIT_CARD',
        'Email': 'EMAIL_ADDRESS',
        'International Banking Account Number (IBAN)': 'IBAN_CODE',
        'IP': 'IP_ADDRESS',
        'Organization': 'NRP',
        'Location': 'LOCATION',
        'Address': 'LOCATION',
        'EU GPS Coordinats': 'LOCATION',
        'Person': 'PERSON',
        'PhoneNumber (US and EU only)': 'PHONE_NUMBER',
        'U.S. Bank Account Number': 'US_BANK_NUMBER',
        "U.S. Driver's License Number": 'US_DRIVER_LICENSE',
        'U.S. Individual Taxpayer Identification Number (ITIN)': 'US_ITIN',
        'U.S. Passport Number': 'US_PASSPORT',
        'U.S. Social Security Number (SSN)': 'US_SSN',
        'U.K. National Health Service (NHS) Number': 'UK_NHS',
        'Event': 'EVENTS',
        'Skill': 'SKILL',
        'URL': 'URL',
        'Quantity_Number': 'QTY_NUMBER',
        'Quantity_Percentage': 'QTY_PERCENTAGE',
        'Quantity_Ordinal': 'QTY_ORDINAL',
        'Quantity_Age': 'AGE',
        'Quantity_Currency': 'MONETARY_VALUE',
        'Quantity_Dimension': 'DIMENSION',
        'Quantity_Temperature': 'TEMPERATURE',
        'Age': 'AGE',
        'Azure DocumentDB Auth Key': 'AZURE_DOCDB_AUTH_KEY',
        'Azure IAAS Database Connection String and Azure SQL Connection String': 'AZURE_IAAS_CONN_STRING',
        'Azure SQL Connection String': 'AZURE_SQL_CONN_STRING',
        'SQL Server Connection String': 'AZURE_SQL_CONN_STRING',
        'Azure IoT Connection String': 'AZURE_IOT_CONNECTION_STRING',
        'Azure Publish Setting Password': 'AZURE_PUBLISH_SETTINGS_PWD',
        'Azure Redis Cache Connection String': 'AZURE_REDIS_CONN_STRING',
        'Azure SAS': 'AZURE_SAS',
        'Azure Service Bus Connection String': 'AZURE_SERVICE_BUS_CONN_STRING',
        'Azure Storage Account Key': 'AZURE_STORAGE_ACC_KEY',
        'Azure Storage Account Key (Generic)': 'AZURE_STORAGE_ACC_KEY',
        'ABA Routing Number': 'ABA_ROUTING_NUMBER',
        'SWIFT Code': 'SWIFT_CODE',
        'Argentina National Identity (DNI) Number': 'AR_DNI',
        'Austria Identity Card': 'AT_ID',
        'Austria Tax Identification Number': 'AT_TAX_ID',
        'Austria Value Added Tax (VAT) Number': 'AT_VAT',
        'Australia Bank Account Number': 'AU_BANK_NUMBER',
        'Australian Business Number': 'AU_BUSINESS_NUMBER',
        'Australian Company Number': 'AU_COMPANY_NUMBER',
        "Australia Driver's License Number": 'AU_DRIVER_LICENSE',
        'Australia Medical Account Number': 'AU_MEDICAL_ACCOUNT',
        'Australia Passport Number': 'AU_PASSPORT',
        'Australia Tax File Number': 'AU_TAX_NUMBER',
        'Belgium National Number': 'BE_NATIONAL_NUMBER',
        'Belgium Value Added Tax Number': 'BE_VAT_NUMBER',
        'Brazil Legal Entity Number (CNPJ)': 'BR_CNPJ',
        'Brazil CPF Number': 'BR_CPF',
        'Brazil National ID Card (RG)': 'BR_RG',
        'Bulgaria Uniform Civil Number': 'BG_UC_NUMBER',
        'Canada Bank Account Number': 'CA_BANK_NUMBER',
        "Canada Driver's license Number": 'CA_DRIVER_LICENSE',
        'Canada Health Service Number': 'CA_HSN',
        'Canada Passport Number': 'CA_PASSPORT',
        'Canada Personal Health Identification Number (PHIN)': 'CA_PHIN',
        'Canada Social Insurance Number': 'CA_SIN',
        'China Resident Identity Card (PRC) Number': 'CN_PRC_NUMBER',
        'Croatia Identity Card Number': 'HR_ID_NUMBER',
        'Croatia National ID Card Number': 'HR_ID_NUMBER',
        'Croatia Personal Identification (OIB) Number': 'HR_OIB_NUMBER',
        'Cyprus Identity Card Number': 'CY_ID_NUMBER',
        'Cyprus Tax Identification Number': 'CY_TAX_NUMBER',
        'Czech Personal Identity Number': 'CZ_ID_NUMBER',
        'Denmark Personal Identification number': 'DK_ID_NUMBER',
        'Estonia Personal Identification Code': 'EE_ID_NUMBER',
        'EU Debit Card Number': 'EU_DEBIT_CARD',
        "EU Driver's License Number": 'EU_DRIVER_LICENSE',
        'EU National Identification Number': 'EU_NATIONAL_ID_NUMBER',
        'EU Passport Number': 'EU_PASSPORT_NUMBER',
        'EU Social Security Number (SSN) or Equivalent ID': 'EU_SSN',
        'EU Tax Identification Number (TIN)': 'EU_TIN',
        'Finland European Health Insurance Number': 'FI_EHIN',
        'Finland National ID': 'FI_ID',
        'Finland Passport Number': 'FI_PASSPORT',
        "France Driver's License Number": 'FR_DRIVER_LICENSE',
        'France Health Insurance Number': 'FR_HIN',
        'France National ID card (CNI)': 'FR_CNI',
        'France Passport Number': 'FR_PASSPORT',
        'France Social Security Number (INSEE)': 'FR_INSEE',
        'France Tax Identification Number (numéro SPI.)': 'FR_SPI_NUMBER',
        'France Value Added Tax Number': 'FR_VAT_NUMBER',
        "German Driver's License Number": 'DE_DRIVER_LICENSE',
        'Germany Identity Card Number': 'DE_ID_NUMBER',
        'German Passport Number': 'DE_PASSPORT',
        'Germany Tax Identification Number': 'DE_TAX_NUMBER',
        'Germany Value Added Tax Number': 'DE_VAT_NUMBER',
        'Greece National ID card number': 'GR_ID_NUMBER',
        'Greece Tax identification Number': 'GR_TAX_NUMBER',
        'Hong Kong Identity Card (HKID) Number': 'HK_ID',
        'Hungary National Identification Number': 'HU_ID',
        'Hungary Tax identification Number': 'HU_TAX_NUMBER',
        'Hungary Value Added Tax Number': 'HU_VAT',
        'India Permanent Account Number (PAN)': 'IN_PAN',
        'India Unique Identification (Aadhaar) Number': 'IN_AADHAAR',
        'Indonesia Identity Card (KTP) Number': 'ID_KTP',
        'Ireland Personal Public Service (PPS) Number': 'IE_PPS',
        'Israel National ID': 'IL_ID',
        'Israel Bank Account Number': 'IL_BANK_NUMBER',
        "Italy Driver's license ID": 'IT_DRIVER_LICENSE',
        'Italy Fiscal Code': 'IT_FISCAL_NUMBER',
        'Italy Value Added Tax Number': 'IT_VAT',
        'Japan Bank Account Number': 'JP_BANK_NUMBER',
        "Japan Driver's License Number": 'JP_DRIVER_LICENSE',
        'Japanese My Number Personal': 'JP_ID',
        'Japanese My Number Corporate': 'JP_BUSINESS_ID',
        'Japan Resident Registration Number': 'JP_RESIDENT_NUMBER',
        'Japanese Residence Card Number': 'JP_RESIDENCE_NUMBER',
        'Japan Social Insurance Number (SIN)': 'JP_SIN',
        'Japan Passport Number': 'JP_PASSPORT',
        'Latvia Personal Code': 'LV_ID',
        'Lithuania Personal Code': 'LT_ID',
        'Luxemburg National Identification Number (Natural persons)': 'LU_ID',
        'Luxemburg National Identification Number (Non-natural persons)': 'LU_ID',
        'Malaysia Identity Card Number': 'MY_ID',
        'Malta Identity Card Number': 'MT_ID',
        'Malta Tax Identification Number': 'MT_TAX_NUMBER',
        "Netherlands Citizen's Service (BSN) Number": 'NL_BSN_NUMBER',
        'Netherlands Tax Identification Number': 'NL_TAX_NUMBER',
        'Netherlands Value Added Tax Number': 'NL_VAT',
        'New Zealand Bank Account Number': 'NZ_BANK_NUMBER',
        "New Zealand Driver's License Number": 'NZ_DRIVER_LICENSE',
        'New Zealand Inland Revenue Number': 'NZ_INLAND_REVENUE',
        'New Zealand Ministry of Health Number': 'NZ_MHN_NUMBER',
        'New Zealand Social Welfare Number': 'NZ_SWN_NUMBER',
        'Norway Identity Number': 'NO_ID',
        'Philippines Unified Multi-Purpose ID Number': 'PH_ID',
        'Poland Identity Card': 'PL_ID',
        'Poland National ID (PESEL)': 'PL_ID',
        'Poland Passport Number': 'PL_PASSPORT',
        'Poland REGON Number': 'PL_REGON_NUMBER',
        'Poland Tax Identification Number': 'PL_TAX_NUMBER',
        'Portugal Citizen Card Number': 'PT_ID',
        'Portugal Tax Identification Number': 'PT_TAX_NUMBER',
        'Romania Personal Numerical Code (CNP)': 'RO_CNP_NUMBER',
        'Russian Passport Number (Domestic)': 'RU_PASSPORT',
        'Russian Passport Number (International)': 'RU_PASSPORT',
        'Saudi Arabia National ID': 'SA_ID',
        'Singapore National Registration ID Card (NRIC) Number': 'SG_NRIC_NUMBER',
        'Slovakia Personal Number': 'SK_ID',
        'Slovenia Tax Identification Number': 'SI_TAX_NUMBER',
        'Slovenia Unique Master Citizen Number': 'SI_ID',
        'South Africa Identification Number': 'ZA_ID',
        'South Korea Resident Registration Number': 'KR_ID',
        'Spain DNI': 'ES_DNI_NUMBER',
        'Spain Social Security Number (SSN)': 'ES_SSN_NUMBER',
        'Spain Tax Identification Number': 'ES_TAX_NUMBER',
        'Sweden National ID': 'SE_ID',
        'Sweden Passport Number': 'SE_PASSPORT',
        'Sweden Tax Identification Number': 'SE_TAX_NUMBER',
        'Swiss Social Security Number AHV': 'CH_AHV_NUMBER',
        'Taiwan National ID': 'TW_ID',
        'Taiwan Resident Certificate (ARC/TARC)': 'TW_TARC',
        'Taiwan Passport Number': 'TW_PASSPORT',
        'Thai Population Identification Code': 'TH_ID',
        'Turkish National Identification Number': 'TR_ID',
        'Ukraine Passport Number (Domestic)': 'UA_PASSPORT',
        'Ukraine Passport Number (International)': 'UA_PASSPORT',
        "U.K. Driver's license Number": 'UK_DRIVER_LICENSE',
        'U.K. Electoral Roll Number': 'UK_ERN_NUMBER',
        'U.K. National Insurance Number (NINO)': 'UK_NINO_NUMBER',
        'U.K. Passport Number': 'UK_PASSPORT',
        'U.K. Unique Taxpayer Reference Number': 'UK_TAX_NUMBER',
        'U.S. Drug Enforcement Agency (DEA) number': 'US_DEA_NUMBER'
    }

class TextAnalyticsRecognizer(RemoteRecognizer):
    """
    Use Azure Text Analytics service to detect PII entities.
    """

    SUPPORTED_ENTITIES = set(TYPES_MAPPING.values())
    DEFAULT_EXPLANATION = "Identified as {} by Text Analytics"

    

    def __init__(self, text_analytics_dal=None, supported_language='en'):
        super().__init__(supported_entities=self.SUPPORTED_ENTITIES,
                         name='Azure Text Analytics',
                         version='3.0-preview.1',
                         supported_language=supported_language)

        if not text_analytics_dal:
            text_analytics_dal = TextAnalyticsDal(self.logger)
        self.dal = text_analytics_dal

    def load(self):
        pass

    def get_supported_entities(self):
        self.logger.debug("get_supported_entities was called")
        return self.SUPPORTED_ENTITIES

    def analyze_text(self, text, entities):
        return self.analyze(text, entities)

    def analyze(self, text, entities, nlp_artifacts=None):
        """
        This is the core method for analyzing text, assuming entities are
        the subset of the supported entities types.
        :param text: The text to be analyzed
        :param entities: The list of entities to be detected
        :param nlp_artifacts: Value of type NlpArtifacts.
        A group of attributes which are the result of
                              some NLP process over the matching text
        :return: list of RecognizerResult
        :rtype: [RecognizerResult]
        """
        self.logger.debug("analyze was called")
        try:
            data = self.dal.analyze_pii_data(text)
            return self.convert_to_analyze_response(data)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error("Failed to execute request to "
                              "Text Analytics. {}", e)
        return None

    def convert_to_analyze_response(self, json_obj):
        result = []

        # None means the recognizer failed to load.
        if json_obj is None:
            return result
        self.logger.info(json_obj)

        svc_response = json_obj
        if not svc_response['documents']:
            if svc_response['errors']:
                self.logger.error('Text Analytics returned error: {}'
                                  .format(str(svc_response['errors'])))
                return result

        for entity in svc_response['documents'][0]['entities']:
            recognizer_result = \
                RecognizerResult(TextAnalyticsRecognizer.
                                 __convert_to_presidio_type(entity['type'], subtype=entity.get('subtype')),
                                 entity['offset'],
                                 entity['offset'] + entity['length'],
                                 entity['score'],
                                 self.DEFAULT_EXPLANATION.format(entity['type']))
            result.append(recognizer_result)
        return result

    @staticmethod
    def __convert_to_presidio_type(ta_type, **kwargs):
        subtype = kwargs.get('subtype', False)
        if subtype:
            presidio_type = '{}_{}'.format(ta_type, subtype)
            return TYPES_MAPPING.get(presidio_type) or TYPES_MAPPING.get(ta_type) or presidio_type
        else:
            return TYPES_MAPPING.get(ta_type) or ta_type