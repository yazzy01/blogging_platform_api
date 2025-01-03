from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

def send_verification_email(request, user):
    """Send email verification link to user"""
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account'
    message = render_to_string('users/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.content_subtype = 'html'
    return email.send()

def send_password_reset_email(request, user):
    """Send password reset link to user"""
    current_site = get_current_site(request)
    mail_subject = 'Reset your blog password'
    message = render_to_string('users/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.content_subtype = 'html'
    return email.send()

def send_login_alert_email(user, ip_address, location=None):
    """Send alert email for suspicious login activity"""
    mail_subject = 'Suspicious login activity detected'
    message = render_to_string('users/login_alert_email.html', {
        'user': user,
        'ip_address': ip_address,
        'location': location,
        'timestamp': user.profile.last_login_at,
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.content_subtype = 'html'
    return email.send()
