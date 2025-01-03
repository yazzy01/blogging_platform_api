from social_core.pipeline.user import get_username as social_get_username
from .settings import SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GITHUB_KEY
from apps.users.models import Profile

def get_username(strategy, details, backend, user=None, *args, **kwargs):
    """Return username for new user"""
    if 'username' not in details:
        return social_get_username(strategy, details, backend, user=user, *args, **kwargs)
    return {'username': details['username']}

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """Create user if not exists"""
    if user:
        return {'is_new': False}

    fields = {'username': details.get('username')}
    
    if backend.name == 'google-oauth2':
        fields['email'] = details.get('email')
        fields['first_name'] = details.get('first_name', '')
        fields['last_name'] = details.get('last_name', '')
    
    elif backend.name == 'github':
        fields['email'] = details.get('email')
        name_parts = details.get('fullname', '').split(' ', 1)
        fields['first_name'] = name_parts[0]
        fields['last_name'] = name_parts[1] if len(name_parts) > 1 else ''

    if not fields['username']:
        fields['username'] = fields['email'].split('@')[0]

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }

def update_user_social_data(backend, strategy, details, response, user=None, *args, **kwargs):
    """Update user data from social provider"""
    if not user:
        return

    # Update profile with social data
    profile = Profile.objects.get_or_create(user=user)[0]
    
    changed = False
    
    # Update avatar if not set
    if not profile.avatar:
        if backend.name == 'google-oauth2' and response.get('picture'):
            profile.avatar = response['picture']
            changed = True
        elif backend.name == 'github' and response.get('avatar_url'):
            profile.avatar = response['avatar_url']
            changed = True
    
    # Update other fields if empty
    if not profile.bio and response.get('bio'):
        profile.bio = response['bio']
        changed = True
        
    if not profile.location and response.get('location'):
        profile.location = response['location']
        changed = True
        
    if not profile.website:
        if backend.name == 'github' and response.get('blog'):
            profile.website = response['blog']
            changed = True
        elif backend.name == 'google-oauth2' and response.get('url'):
            profile.website = response['url']
            changed = True
    
    # Update social links
    if backend.name == 'github' and not profile.github:
        profile.github = response.get('html_url', '')
        changed = True
        
    if changed:
        profile.save()

def validate_social_auth(backend, strategy, details, response, *args, **kwargs):
    """Validate social authentication"""
    if not details.get('email'):
        return strategy.redirect(
            f'/auth/error?message=Email is required for {backend.name} authentication'
        )
    
    if backend.name == 'google-oauth2' and not SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
        return strategy.redirect('/auth/error?message=Google authentication is not configured')
        
    if backend.name == 'github' and not SOCIAL_AUTH_GITHUB_KEY:
        return strategy.redirect('/auth/error?message=GitHub authentication is not configured')
