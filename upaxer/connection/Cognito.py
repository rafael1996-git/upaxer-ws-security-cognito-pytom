import hmac
import hashlib
import base64
import boto3
import os
from upaxer.utils.Secret import get_secret
from upaxer.utils.Constants import AUTH_FLOW, REFRESH_TOKEN
from upaxer.utils.Security import get_secret_hash


class Cognito:
    def __init__(self):
        #config = get_secret(os.environ['SECRET_COGNITO'])
        config = get_secret('com/upax/upaxer/security/cognito/cognitoacount')
        self.poolIdGeneric = config['generic']['poolId']
        self.clientIdGeneric = config['generic']['clientId']
        self.clientSecretGeneric = config['generic']['clientSecret']
        self.poolIdApp = config['app']['poolId']
        self.clientIdApp = config['app']['clientId']
        self.clientSecretApp = config['app']['clientSecret']
        self.client = boto3.client('cognito-idp', region_name='us-east-1')

    def create_user(self, username, password):
        try:
            data = self.client.sign_up(
                ClientId=self.clientIdGeneric,
                Username=username,
                Password=password
            )
            data = self.client.admin_confirm_sign_up(
                UserPoolId=self.poolIdGeneric,
                Username=username
            )
            response = {
                'hasError': False,
                'response': data
            }
        except self.client.exceptions.UsernameExistsException as e:
            response = {
                'hasError': True,
                'response': str(e)
            }
        except Exception as e:
            response = {
                'hasError': True,
                'response': str(e)
            }
        return response

    def generate_auth_token(self, username, password):
        try:
            data = self.client.admin_initiate_auth(
                UserPoolId=self.poolIdGeneric,
                ClientId=self.clientIdGeneric,
                AuthFlow=AUTH_FLOW,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            response = {
                'hasError': False,
                'response': data
            }
        except Exception as e:
            response = {
                'hasError': True,
                'response': str(e)
            }
        return response

    def refresh_token(self, username, token):
        try:
            data = self.client.admin_initiate_auth(
                UserPoolId=self.poolId,
                ClientId=self.clientId,
                AuthFlow=REFRESH_TOKEN,
                AuthParameters={
                    'REFRESH_TOKEN': token,
                    'SECRET_HASH': get_secret_hash(username=username, clientSecret=self.clientSecret,
                                                   clientId=self.clientId),
                    'DEVICE_KEY': ''
                }
            )
            response = {
                'hasError': False,
                'response': data
            }
        except Exception as e:
            response = {
                'hasError': True,
                'response': str(e)
            }
        return response

    def generate_user_auth_token(self, username, password):
        try:
            data = self.client.admin_initiate_auth(
                UserPoolId=self.poolIdApp,
                ClientId=self.clientIdApp,
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'SECRET_HASH': Cognito().get_secret_hash(username),
                    'PASSWORD': password
                },
                ClientMetadata={
                    'username': username,
                    'password': password
                }
            )
            response = {
                'hasError': False,
                'response': data
            }
        except Exception as e:
            response = {
                'hasError': True,
                'response': str(e)
            }
        return response

    def get_secret_hash(self, username):
        msg = username + self.clientIdApp
        dig = hmac.new(str(self.clientSecretApp).encode('utf-8'),
                       msg=str(msg).encode('utf-8'),
                       digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def sign_up(self, phone_code, phone_number, password):
        self.client.sign_up(
            ClientId=self.clientIdApp,
            SecretHash=self.get_secret_hash(phone_number),
            Username=phone_number,
            Password=password,
            UserAttributes=[
                {
                    'Name': "phone_number",
                    'Value': phone_code + phone_number
                }
            ],
            ValidationData=[
                {
                    'Name': "phone_number",
                    'Value': phone_code + phone_number
                }
            ]
        )
        self.confirm(phone_number)

    def confirm(self, phone_number):
        self.client.admin_confirm_sign_up(
            UserPoolId=self.poolIdApp,
            Username=phone_number
        )
