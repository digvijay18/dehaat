# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from order.models import Order


class Ledger(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ledgers')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_ledgers')
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=False)
    post_balance = models.FloatField(null=False)


class Invoice(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_invoices')
    amount = models.FloatField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
