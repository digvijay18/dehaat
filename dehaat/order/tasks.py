from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def send_order_acceptance_sms_to_primary_mobile(amount, order_id, mobile):
    """
    Celery task to send SMS to received mobile number
    """
    print('Order confirmed (Order Id: {0}). Confirmed Total: Rs. {1}/-.'
          ' Your contact number with us: {2}'.format(order_id, amount, mobile))
