from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.permissions import AllowAny
from django.db import connection
from rest_framework.schemas import AutoSchema

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
    
    return response

class HealthCheckSchema(AutoSchema):
    def get_description(self, path, method):
        return "Health check endpoint to verify API is running"

@api_view(['GET'])
@permission_classes([AllowAny])
@schema(HealthCheckSchema())
def health_check(request):
    """
    Health check endpoint to verify API is running
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return Response({
            'status': 'healthy',
            'database': 'connected'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
