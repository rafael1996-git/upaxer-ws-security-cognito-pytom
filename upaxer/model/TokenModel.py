import json
import upaxer.utils.FunctionsDB as FN
import upaxer.utils.Constants as VAR
from upaxer.connection.Oracle import Oracle as ODB
from upaxer.connection.Cognito import Cognito as COG


class TokenModel:

    @staticmethod
    def get_user_credentials():
        parameters = {
            'PARAMETERID': VAR.GENERIC_UPAXER
        }
        result = ODB().execute(type=VAR.TYPE_RETURN_STRING, name=FN.GET_USER_CREDENTIALS, parameters=parameters)
        return result['data']

    @staticmethod
    def get_generic_token(username, password):
        generic_token = COG().generate_auth_token(username=username, password=password)
        if generic_token['hasError']:
            COG().create_user(username, password)
            return TokenModel.get_generic_token(username, password)
        else:
            return generic_token['response']['AuthenticationResult']

    @staticmethod
    def get_user_token(username, password):
        user_token = COG().generate_user_auth_token(username=username, password=password)
        return user_token

    @staticmethod
    def get_user_info_pw(phone_number, password):
        parameters = {
            'phone_number': phone_number,
            'password': password
        }
        data = json.loads(ODB().execute(type=VAR.TYPE_RETURN_CURSOR, name=FN.GET_USER_INFO_PW, parameters=parameters)['data'])
        user = ()
        for item in data:
            user = item
        return user
