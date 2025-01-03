from django.utils.deprecation import MiddlewareMixin
from .models.activity import UserActivity

class UserActivityMiddleware(MiddlewareMixin):
    """Middleware to track user activities"""
    
    def process_request(self, request):
        """Process incoming request"""
        # Store request in thread local storage
        request.activity_tracked = False

    def process_response(self, request, response):
        """Process outgoing response"""
        # Only track activity for authenticated users
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return response

        # Avoid tracking if already tracked (e.g., by a view)
        if getattr(request, 'activity_tracked', False):
            return response

        # Only track certain types of requests
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            activity_type = None
            
            # Determine activity type based on path and method
            if 'posts' in request.path:
                if request.method == 'POST':
                    activity_type = 'post_create'
                elif request.method in ['PUT', 'PATCH']:
                    activity_type = 'post_update'
                elif request.method == 'DELETE':
                    activity_type = 'post_delete'
            
            elif 'comments' in request.path:
                if request.method == 'POST':
                    activity_type = 'comment_create'
                elif request.method in ['PUT', 'PATCH']:
                    activity_type = 'comment_update'
                elif request.method == 'DELETE':
                    activity_type = 'comment_delete'
            
            elif 'profile' in request.path and request.method in ['PUT', 'PATCH']:
                activity_type = 'profile_update'
            
            # Log activity if type was determined
            if activity_type:
                UserActivity.log_activity(
                    user=request.user,
                    activity_type=activity_type,
                    request=request
                )

        return response
