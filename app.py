import logging
import upaxer.utils.Constants as var
from flask import Flask, request
from flask_cors import CORS, cross_origin
from upaxer.controller.TokenController import TokenController as TC

logging.getLogger().setLevel(logging.INFO)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route(var.MAIN_PATH + '/get-generic-token', methods=['POST'])
@cross_origin()
def get_generic_token():
    parameters = request.json
    response = TC(parameters=parameters).get_generic_token()
    return response.create()


@app.route(var.MAIN_PATH + '/get-user-token', methods=['POST'])
@cross_origin()
def get_user_token():
    parameters = request.json
    response = TC(parameters=parameters).get_user_token()
    return response.create()


@app.errorhandler(500)
def internal_server_error(e):
    data = str(e.original_exception)
return {
               'code': 'UPX500',
               'success': False,
               'response': data
           }, 500


if __name__ == '__main__':
    app.run()
