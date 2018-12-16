import apiai
from flask import json

from ..app import app

class DialogFlowV1:
    def __init__(self):
        self.provider = "dialogflow"
        self.openai = apiai.ApiAI(app.config['DIALOGFLOW_API_KEY'])

    def call(self, felix_request):
        dialogflow_result = self.textRequest(felix_request.getSessionId(), felix_request.getQueryText())
        dfResult = json.loads(dialogflow_result);
        return dfResult

    def textRequest(self, sessionId, text):
        request = self.openai.text_request()
        #request.lang = 'en'
        request.lang = 'es'
        request.session_id = sessionId
        request.query = text
        self.apiaiResponse = request.getresponse().read().decode('utf8')

        return self.apiaiResponse

    def hasParameters(self, parameters):
        if len(parameters)==0:
            return False

        emptyKeys = 0
        for key, value in parameters.items():
            if len(value)==0:
                emptyKeys += 1

        return len(parameters)-emptyKeys > 0

