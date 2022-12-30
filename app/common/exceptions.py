from typing import List
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.db import IntegrityError

def handle_exception(exception, context):
    response = exception_handler(exception, context)

    if isinstance(exception, IntegrityError) and not response:
        return handle_integrity_error(exception)

    return response

def handle_integrity_error(exception):
    message = "An error occur"
    error_message: str = exception.args[0]
    
    if "UNIQUE" in error_message:
        message = "The registry already exist"

    data = { "details": message }

    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
