from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models.base import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model"""
    class Meta:
        model = Profile
        fields = ('id', 'user', 'avatar', 'bio', 'location', 'website', 
                 'birth_date', 'twitter', 'github', 'linkedin')
        read_only_fields = ('user',)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User with Profile data"""
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance
