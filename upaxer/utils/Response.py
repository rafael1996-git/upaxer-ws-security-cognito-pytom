from datetime import datetime


class Response:
    def __init__(self, status, data=None, message=None):
        self.status = status
        self.message = message
        self.data = data
        self.response = None

    def create(self):
        self.response = {
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'code': self.status,
            'message': self.message,
            'response': self.data
        }
        return self.response
