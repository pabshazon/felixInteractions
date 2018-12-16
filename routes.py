from flask import request, json

from .app import app
from .services import NLPService, HSDataService
from .responses import felixResponse
from .requests import felixRequest

# @todo: manage session expiration times
# @todo: manage authorization key and tokens


@app.route('/')
def hello_world():
    return json.dumps('Hello Felix!')

@app.route('/search')
def search():
    felix_request = felixRequest.Request(request.args)
    felix_request.addNLP(NLPService.DialogFlowV1().call(felix_request))  # @todo: abstract to use multiple NLP providers
    human_services_data = HSDataService.OhanaService().call(felix_request)  # @todo: abstract to use multiple HSD providers

    # @todo refactor this below
    response = felixResponse.Response(felix_request)
    response.addText(felix_request.getNlpAnswerText())
    response.addData(human_services_data)

    # @todo: save request response data
    # response.getSessionId() - la session ID usada
    # felix_request.getQueryText() - el texto que dijo el usuario
    # felix_request.getNlpAnswerText() - la respuesta que va a decir el asistente
    # saveInteractionDataToDb(response)

    return response.toJson()

