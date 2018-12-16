from flask import json, jsonify
from base64 import b64encode
import os

from ..app import app

# @todo: how can I make the builder pattern with python, obtaining an immutable object after builder.build()
class Response:
    def __init__(self, felix_request):

        self.request = felix_request
        self.response = {
            'success': 'true',
            'sessionId': self.validateSession()
        }

    def validateSession(self):
        # new app for now @todo-wip new session management from android side
        if self.request.getSessionId() is None:
            return self.assignNewSessionId()

        # @ @todo sessionIdIsExpired is not implemented
        elif self.sessionIdHasExpired():
            return self.assignNewSessionId()

        elif self.request.isActionValidAndComplete():  # @CONTRACT with apps, we renew session when action is completed
            return self.assignNewSessionId()

        return self.request.getSessionId()

    def assignNewSessionId(self):
        sessionId = os.urandom(16)
        return b64encode(sessionId).decode('utf-8')

    def sessionIdHasExpired(self):
        #@todo functionality not developed
        return False

    '''
    -----
    Add methods
    -----    
    '''

    def addSessionId(self, sessionId):
        self.response['sessionId'] = sessionId

    def addData(self, data):
        if self.isDataValid(data):
            self.response['data'] = data
        else:
            self.response['data'] = []

    def addText(self, text):
        self.response['text'] = text  # @todo validate input

    '''
    GETTERS
    '''
    def getSessionId(self):
        return self.response['sessionId']

    '''
    VALIDATORS
    '''

    def isDataValid(self, data):
        if data == "NoResultsInDb":  # @in this case data is empty because the Ohana Server lacks data. This info in direct potential improvement.
            self.response['text'] = app.config['EMPTY_RESULT_TEXT']
            return False

        return True

    def toJson(self):
        return json.dumps(self.response)
