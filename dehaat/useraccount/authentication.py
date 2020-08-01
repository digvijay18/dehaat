from rest_framework import authentication
from rest_framework import exceptions

from django.core.cache import cache
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class OTPAuthentication(authentication.BaseAuthentication):
    """
    Customized authentication class to manage both types of authentication-
    1. otp & device token authentication for customer
    2. username & password authentication for admin/agent
    """
    def authenticate(self, request):
        identifier = request.META.get('HTTP_X_REQUEST_ID')
        if not identifier:
            username = request.data.get('username')
            password = request.data.get('password')
            if not (username and password):
                # If no identifier, and no username-password, authentication fail
                raise exceptions.AuthenticationFailed('Username/Password were not provided.')

            # Normal django-based authentication for username, password
            user = authenticate(username=username, password=password)
            return user, None

        # Reaches here when device token found. Get otp.
        user_code = str(request.data.get('otp', None))
        value = None

        # Attempt to get otp and user stored for this device id in redis cache.
        if identifier and cache.has_key(identifier):
            value = cache.get(identifier)
            cache.delete(identifier)

        # If attempt fails, authentication fails.
        if not value:
            raise exceptions.AuthenticationFailed('OTP timed out. Please try again.')

        correct_code, user_id = value.split(':')

        # If wrong OTP is entered, fail/
        if correct_code != user_code:
            raise exceptions.AuthenticationFailed('Invalid OTP code. Please try again.')

        # Attempt to get and return corresponding user object and return.
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None, None

        return user, None
