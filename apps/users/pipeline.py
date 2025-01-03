def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    """Get user's avatar from social provider"""
    if not user:
        return

    if backend.name == 'google-oauth2':
        if response.get('picture'):
            user.profile.avatar = response['picture']
            user.profile.save()

    elif backend.name == 'github':
        if response.get('avatar_url'):
            user.profile.avatar = response['avatar_url']
            user.profile.save()

    return None
