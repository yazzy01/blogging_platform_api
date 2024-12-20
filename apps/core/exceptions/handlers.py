from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, DjangoValidationError):
            return Response({
                'error': 'Validation Error',
                'detail': exc.message_dict if hasattr(exc, 'message_dict') else str(exc),
                'status_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'An unexpected error occurred',
            'detail': str(exc),
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add request information
    request = context.get('request')
    if request:
        response.data['path'] = request.path
        response.data['method'] = request.method

    # Customize error responses
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        response.data = {
            'error': 'Validation Error',
            'details': response.data,
            'status_code': status.HTTP_400_BAD_REQUEST
        }

    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            'error': 'Authentication Failed',
            'detail': response.data.get('detail', 'Unauthorized access'),
            'status_code': status.HTTP_401_UNAUTHORIZED
        }

    elif response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            'error': 'Permission Denied',
            'detail': response.data.get('detail', 'You do not have permission to perform this action'),
            'status_code': status.HTTP_403_FORBIDDEN
        }

    return response
