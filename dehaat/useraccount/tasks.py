from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def send_otp_to_primary_mobile(otp, mobile):
    """
    Send OTP to given mobile number.
    """
    print('Sending otp to mobile: ', otp, mobile)
