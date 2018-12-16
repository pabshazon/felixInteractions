import requests
from flask import json

from felixInteractionsServer.app import app
from ..app import app

class OhanaService:  # @ todo abstract into multiple HSData providers
    def __init__(self):
        self.data_service_url = app.config['OHANA_URL']

    def call(self, flx_request):
        if flx_request.isActionValidAndComplete():
            return self.getLocationsFromOhana(flx_request)

        else:
            return []

    def getLocationsFromOhana(self, felix_request):
        ohana_uri = self.generateGetUriCall(felix_request)
        ohana_results = requests.get(ohana_uri)
        return json.loads(ohana_results.text)

    def generateGetUriCall(self, felix_request):
        ohana_uri = self.data_service_url + "/search?lat_lng=" + felix_request.getLat() + \
                    "," + felix_request.getLng() + "&category=" + felix_request.getAction()

        parameters_dict = felix_request.getNlpParameters()
        if felix_request.hasParameters(parameters_dict):
            parameters = ",".join(parameters_dict.values())
            ohana_uri += "&keyword=" + parameters

        return ohana_uri
