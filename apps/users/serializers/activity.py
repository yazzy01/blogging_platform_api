from rest_framework import serializers
from ..models.activity import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for user activities"""
    content_type = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()
    
    class Meta:
        model = UserActivity
        fields = ('id', 'user', 'activity_type', 'timestamp', 'ip_address',
                 'content_type', 'content_object', 'metadata')
        read_only_fields = fields

    def get_content_type(self, obj):
        """Get string representation of content type"""
        if obj.content_type:
            return obj.content_type.model
        return None

    def get_content_object(self, obj):
        """Get basic representation of related object"""
        if obj.content_object:
            if hasattr(obj.content_object, 'title'):
                return {'id': obj.object_id, 'title': obj.content_object.title}
            elif hasattr(obj.content_object, 'content'):
                return {'id': obj.object_id, 'content': str(obj.content_object.content)[:100]}
            return {'id': obj.object_id}
        return None
