import os
from base64 import b64encode

# @todo: how can I make the builder pattern with python, obtaining an immutable object after builder.build()
class Request:
    def __init__(self, args):
        self.sessionId = args.get('sessionId')
        if not self.isSessionValid():
            self.sessionId = self.assignNewSessionId()

        self.query_text = args.get('queryText')
        self.lat = args.get('lat')
        self.lng = args.get('lng')
        self.allowedActions = ['Medical%20Care', 'Food', 'FX-ID', 'FX-Job', 'FX-Legal', 'Housing', 'Transit', 'Hygiene',
                          'Personal%20Hygiene', ]  # @todo: refactor separate code from data
        self.request = {
            'sessionId': self.sessionId
        }

    def getSessionId(self):
        return self.request['sessionId']

    def getQueryText(self):
        return self.query_text

    def getNlpAnswerText(self):
        return self.nlp['result']['fulfillment']['speech']

    def getAction(self):
        return self.nlp['result']['action']

    def getLat(self):
        return self.lat

    def getLng(self):
        return self.lng

    def getNlpParameters(self):
        return self.nlp['result']['parameters']

    def addLatLong(self, lat, long):
        self.lat = lat
        self.lng = long  # @todo validate

    def addNLP(self, nlpServiceResponse):
        self.nlp = nlpServiceResponse  # @todo validate


    def addPhone(self, phone):
        self.phone = phone  # @todo validate

    def isActionValid(self):
        if self.nlp['result']['action'] in self.allowedActions:
            return True
        else:
            return False

    def isActionComplete(self):
        return not self.nlp['result']['actionIncomplete']

    def isActionValidAndComplete(self):
        if self.isActionValid():
            return self.isActionComplete()
        else:
            return False

    def assignNewSessionId(self):
        sessionId = os.urandom(16) # @todo cambiar urandom por timestamp+telefono+hashed
        return b64encode(sessionId).decode('utf-8')

    def hasParameters(self, parameters):
        if len(parameters)==0:
            return False

        emptyKeys = 0
        for key, value in parameters.items():
            if len(value)==0:
                emptyKeys += 1

        return len(parameters)-emptyKeys > 0

    def isSessionValid(self):
        if self.sessionId is None:
            return False

        elif self.sessionId == "":
            return False

        return True

