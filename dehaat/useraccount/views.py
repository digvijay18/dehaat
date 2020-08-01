# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
import random

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication

from django.core.cache import cache
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from . import serializers
from .tasks import send_otp_to_primary_mobile
from .authentication import OTPAuthentication
from dehaat.settings import ADMIN_GROUP, AGENT_GROUP


@method_decorator(csrf_exempt, 'dispatch')
class LoginMobileNumber(APIView):
    """
    An end-point to generate an OTP for a mobile number login. Requires 10 digit mobile number.
    Responds with a one-time device id header so that login happens from same client.
    Also, currently responds with OTP response (for convenient verification).
    Read API Contract for use.
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        mobile = request.GET.get('mobile', None)
        # If no number found or has alphabets or not 10 digits, return with error.
        if not (mobile and len(mobile) == 10 and mobile.isnumeric()):
            return Response({'err': 'Mobile Number is invalid.'}, status.HTTP_400_BAD_REQUEST)

        # If mobile not registered, throw error.
        try:
            user = User.objects.get(username=mobile)
        except User.DoesNotExist:
            return Response({'err': 'Number Not Found'}, status.HTTP_204_NO_CONTENT)

        # OTP generation and one time device token generation
        otp = str(random.randint(1000, 9999))
        device_identifier = str(uuid.uuid4())

        # Set combination in redis cache and send async SMS through rabbitmq consumer
        cache.set(device_identifier, otp + ':' + str(user.id), 60)
        send_otp_to_primary_mobile.delay(otp, mobile)

        # Set token in header and respond
        response = Response({'otp': otp})
        response['X-Request-Id'] = device_identifier
        return response


@method_decorator(csrf_exempt, 'dispatch')
class Login(APIView):
    """
    Logs user in through two ways. It either accepts username and password, or
    it accepts a valid otp and device token.
    Read API contract for use.
    """
    authentication_classes = [SessionAuthentication, OTPAuthentication]

    def post(self, request, *args, **kwargs):
        if request.user is None:
            return Response({'err': 'Unable to verify. Please try again.'}, status.HTTP_406_NOT_ACCEPTABLE)

        # Log in if user authenticated and return.
        login(request, request.user)
        return Response({'data': {'message:': 'You are now Logged in.'}}, status.HTTP_200_OK)


class Logout(APIView):
    """
    Logs out a session.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'msg': 'You are now logged out.'}, status.HTTP_205_RESET_CONTENT)


class Account(generics.CreateAPIView):
    """
    Create an account with username and password. username can be a mobile number.
    Read API contract for use.
    """
    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserAccountSerializer

    def perform_create(self, serializer):
        data = serializer.data
        g_name = data.pop('groups')
        email = data.pop('email', '')

        # Get relevant role
        group = Group.objects.filter(name=g_name).first()
        if g_name == ADMIN_GROUP:
            user = User.objects.create_superuser(email=email, **data)
        elif g_name == AGENT_GROUP:
            user = User.objects.create_user(is_staff=True, email=email, **data)
        else:
            user = User.objects.create_user(email=email, **data)

        user.groups.add(group)
