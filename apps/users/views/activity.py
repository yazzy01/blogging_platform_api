from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ..models.activity import UserActivity
from ..serializers.activity import UserActivitySerializer

class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user activities"""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return activities for the current user,
        or all activities for staff users
        """
        if getattr(self, 'swagger_fake_view', False):
            return UserActivity.objects.none()
        if self.request.user.is_staff:
            return UserActivity.objects.all()
        return UserActivity.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics for the user"""
        # Get base queryset
        queryset = self.get_queryset()
        
        # Get time range from query params (default to last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Get activity counts by type
        activity_counts = (queryset
            .filter(timestamp__gte=start_date)
            .values('activity_type')
            .annotate(count=Count('id'))
            .order_by('-count'))
        
        # Get recent activities
        recent_activities = (queryset
            .select_related('user')
            .order_by('-timestamp')[:10])
        
        # Get activity trend (daily counts for the period)
        trend = (queryset
            .filter(timestamp__gte=start_date)
            .extra({'date': "date(timestamp)"})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date'))
        
        return Response({
            'activity_counts': activity_counts,
            'recent_activities': UserActivitySerializer(recent_activities, many=True).data,
            'trend': trend,
        })

    @action(detail=False, methods=['get'])
    def most_active_times(self, request):
        """Get the most active times for the user"""
        queryset = self.get_queryset()
        
        # Get hour of day activity distribution
        hour_distribution = (queryset
            .extra({'hour': "EXTRACT(hour FROM timestamp)"})
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour'))
        
        # Get day of week activity distribution
        day_distribution = (queryset
            .extra({'day': "EXTRACT(dow FROM timestamp)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day'))
        
        return Response({
            'hour_distribution': hour_distribution,
            'day_distribution': day_distribution,
        })
