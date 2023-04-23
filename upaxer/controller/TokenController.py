from upaxer.utils.Response import Response
from upaxer.model.TokenModel import TokenModel as TM
from upaxer.connection.Cognito import Cognito as COG


class TokenController:
    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def get_generic_token():
        user_credentials = TM().get_user_credentials()
        username = 'UpaxerCognito'
        password = user_credentials
        generic_token = TM().get_generic_token(username=username, password=password)
        response = {
            'token': generic_token['TokenType'] + ' ' + generic_token['IdToken']
        }
        return Response(status='UPX200', data=response, message='Exitoso')

    def get_user_token(self):
        user_exist = TM.get_user_info_pw(phone_number=self.parameters['phoneNumber'], password=self.parameters['password'])
        if user_exist:
            user_token = TM().get_user_token(username=self.parameters['phoneNumber'], password=self.parameters['password'])
            if not user_token['hasError']:
                user_token = user_token['response']['AuthenticationResult']
                response = {
                    'token': user_token['TokenType'] + ' ' + user_token['IdToken']
                }
                return Response(status='UPX200', data=response, message='Exitoso')
            else:
                COG().sign_up(phone_code=user_exist['PHONE_CODE'], phone_number=self.parameters['phoneNumber'], password=self.parameters['password'])
                user_token = TM().get_user_token(username=self.parameters['phoneNumber'],
                                                 password=self.parameters['password'])
                user_token = user_token['response']['AuthenticationResult']
                response = {
                    'token': user_token['TokenType'] + ' ' + user_token['IdToken']
                }
                return Response(status='UPX200', data=response, message='Exitoso')
        else:
            return Response(status='UPX300', data='user does not exist', message='Fallido')

