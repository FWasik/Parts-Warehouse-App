from rest_framework.exceptions import APIException

class CustomException(APIException):
    default_code = 500
    default_detail = {'message': 'Error occurred'}

    def __init__(self, message, status_code):
        self.detail = {'message': message}
        self.status_code = status_code