from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

def custom_404(request, exception):
    """
    Custom handler for 404 errors
    """
    data = {
        'error': 'The requested resource was not found',
        'status_code': 404
    }
    return JsonResponse(data, status=404)

def custom_500(request):
    """
    Custom handler for 500 errors
    """
    data = {
        'error': 'An internal server error occurred',
        'status_code': 500
    }
    return JsonResponse(data, status=500)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST framework
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        
        # Add more context if available
        if hasattr(exc, 'detail'):
            response.data['detail'] = str(exc.detail)
        
        # Add request information
        response.data['path'] = context['request'].path
        response.data['method'] = context['request'].method

    return response
