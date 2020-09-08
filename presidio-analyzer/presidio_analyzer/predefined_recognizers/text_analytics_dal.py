import http
import requests
import os


class TextAnalyticsDal:
    def __init__(self, logger, tolerate_errors=True):
        """
        Create a new instance of TextAnalyticsDal.
        :param logger: A logger.
        :param tolerate_errors: When set to True (default),
        the analyzer will complete initialization.
        When False, exception is thrown if required data
        is missing.
        """
        self.logger = logger
        self.tolerate_errors = tolerate_errors
        self.endpoint = os.environ.get('TEXT_ANALYTICS_ENDPOINT', 'https://skyfer-pii-detector.cognitiveservices.azure.com')
        self.key = os.environ.get('TEXT_ANALYTICS_KEY', '9d5287acaea6414c9206942062ef0bee')
        self.api_path = '/text/analytics/v3.0-preview.1/entities/recognition/'
        self.api_classes = ['general', 'pii'] # request both general data and pii data 
        self.failed_to_load = False

        error_message = 'TextAnalyticsRecognizer cannot work without {}.'
        if not self.endpoint:
            self.failed_to_load = True
            self.logger.error(error_message.format('an endpoint'))
            if not self.tolerate_errors:
                raise ValueError(error_message.format('an endpoint'))

        if not self.key:
            self.failed_to_load = True
            self.logger.error(error_message.format('a key'))
            if not self.tolerate_errors:
                raise ValueError(error_message.format('a key'))

        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }

    def analyze_pii_data(self, text):
        """
        Analyze the text using TextAnalytics PII service
        :param text: The text to be analyzed
        :return: json string
        """
        if self.failed_to_load:
            return None

        body = {
            "Documents": [
                {
                    "Language": "en",
                    "Id": "0",
                    "Text": text
                },
            ]
        }
        params = {
            'domain': 'phi',
            'model-version': '2020-04-01'
        }
        data = None
        try:
            for c in self.api_classes:
                req = requests.post(self.endpoint+self.api_path+c, json=body, headers=self.headers, params=params)
                d = req.json()

                if data is None:
                    data = d
                else:
                    data['documents'].extend(d['documents'])
        except Exception as e:
            self.logger.error("Could not request Text Analytics service", e)

        return data