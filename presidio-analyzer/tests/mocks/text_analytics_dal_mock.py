import json

class TextAnalyticsDalMock:
    def __init__(self, mock_response):
        self.mock_response = json.loads(mock_response)

    def analyze_pii_data(self, text):
        return self.mock_response