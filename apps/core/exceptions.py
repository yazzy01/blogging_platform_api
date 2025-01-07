from rest_framework.exceptions import APIException
from rest_framework import status


class ResourceNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'resource_not_found'


class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'


# Explicitly expose these classes
__all__ = ['ResourceNotFoundError', 'PermissionDeniedError']
