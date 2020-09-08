import json
from presidio_analyzer import RemoteRecognizer, RecognizerResult

from presidio_analyzer.predefined_recognizers.text_analytics_dal \
    import TextAnalyticsDal


TYPES_MAPPING = {
        'Product': 'COMPUTER_PRODUCTS',
        'DateTime': 'DATE_TIME',
        'PersonType': 'PERSON_JOB',
        'Credit Card': 'CREDIT_CARD',
        'Email': 'EMAIL_ADDRESS',
        'International Banking Account Number (IBAN)': 'IBAN_CODE',
        'IP': 'IP_ADDRESS',
        'Organization': 'NRP',
        'Location': 'LOCATION',
        'Address': 'LOCATION',
        'EU GPS Coordinats': 'LOCATION',
        'Person': 'PERSON',
        'PhoneNumber (US and EU only)': 'PHONE_NUMBER'
    }

class TextAnalyticsRecognizer(RemoteRecognizer):
    """
    Use Azure Text Analytics service to detect PII entities.
    """

    SUPPORTED_ENTITIES = [
        "DATE_TIME", 
        "EMAIL_ADDRESS", 
        "IP_ADDRESS", 
        "PERSON", 
        "PHONE_NUMBER", 
        "LOCATION", 
        "NRP", 
        "PERSON_JOB",
        "COMPUTER_PRODUCTS"
    ]
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
                                 __convert_to_presidio_type(entity['type']),
                                 entity['offset'],
                                 entity['offset'] + entity['length'],
                                 entity['score'],
                                 self.DEFAULT_EXPLANATION.format(entity['type']))
            result.append(recognizer_result)
        return result

    @staticmethod
    def __convert_to_presidio_type(ta_type):
        return TYPES_MAPPING.get(ta_type, ta_type)