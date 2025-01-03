from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework.response import Response
import logging

logger = logging.getLogger('apps')

class BaseAPIException(APIException):
    """Base exception for custom API exceptions"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    default_code = 'error'

class InvalidInputError(BaseAPIException):
    """Exception raised when input validation fails"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid_input'

class ResourceNotFoundError(BaseAPIException):
    """Exception raised when a requested resource is not found"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'

class PermissionDeniedError(BaseAPIException):
    """Exception raised when user doesn't have required permissions"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'

def custom_exception_handler(exc, context):
    """Custom exception handler for standardized error responses"""
    
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Log the error
    logger.error(f"Exception occurred: {exc}", exc_info=True, extra={
        'view': context['view'].__class__.__name__,
        'request_path': context['request'].path,
        'request_method': context['request'].method,
    })

    # If unexpected error occurs
    if response is None:
        if isinstance(exc, DjangoValidationError):
            data = {
                'error': 'validation_error',
                'detail': exc.messages[0] if exc.messages else str(exc),
                'fields': exc.message_dict if hasattr(exc, 'message_dict') else None
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if isinstance(exc, Http404):
            data = {
                'error': 'not_found',
                'detail': 'Resource not found.'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
        # Handle unexpected exceptions
        data = {
            'error': 'internal_server_error',
            'detail': 'An unexpected error occurred.'
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Standardize the error response format
    if response is not None:
        error_data = {
            'error': response.status_text.lower().replace(' ', '_'),
            'detail': response.data.get('detail', str(response.data)) if isinstance(response.data, dict) else str(response.data)
        }
        
        # Add field errors if present
        if isinstance(response.data, dict) and any(isinstance(v, list) for v in response.data.values()):
            error_data['fields'] = {k: v for k, v in response.data.items() if isinstance(v, list)}
        
        response.data = error_data

    return response
